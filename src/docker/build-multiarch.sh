#!/bin/bash
# RXiv-Maker Multi-Architecture Docker Build and Upload Script
# Unified script for building, testing, and pushing multi-architecture images

set -e

# =====================================
# Configuration and Colors
# =====================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Docker configuration
IMAGE_NAME="${IMAGE_NAME:-rxiv-maker}"
REGISTRY="${REGISTRY:-docker.io}"
NAMESPACE="${NAMESPACE:-$(whoami)}"
PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"
TAG="${TAG:-latest}"

# Full image reference
FULL_IMAGE="${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}"

# =====================================
# Utility Functions
# =====================================
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_header() {
    echo -e "${BOLD}${CYAN}$1${NC}"
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        echo "Please install Docker from https://docker.com/get-started"
        exit 1
    fi

    # Check if buildx is available
    if ! docker buildx version &> /dev/null; then
        log_error "Docker Buildx is not available"
        echo "Please install Docker Buildx or use a newer version of Docker"
        exit 1
    fi

    log_success "Dependencies check passed"
}

# Setup buildx builder
setup_builder() {
    local builder_name="rxiv-maker-builder"

    log_info "Setting up multi-architecture builder..."

    # Create builder if it doesn't exist
    if ! docker buildx ls | grep -q "$builder_name"; then
        log_info "Creating new buildx builder: $builder_name"
        docker buildx create --name "$builder_name" --driver docker-container --bootstrap
    fi

    # Use the builder
    docker buildx use "$builder_name"

    # Inspect builder to ensure platforms are available
    log_info "Available platforms:"
    docker buildx inspect --bootstrap | grep "Platforms:" || true

    log_success "Builder setup completed"
}

# Build multi-architecture images
build_multiarch() {
    local push="${1:-false}"
    local cache_from=""
    local cache_to=""
    local output_type="docker"

    log_header "Building Multi-Architecture Images"

    cd "$PROJECT_ROOT"

    # Setup cache
    if [[ "$push" == "true" ]]; then
        cache_from="--cache-from=type=registry,ref=${FULL_IMAGE}:buildcache"
        cache_to="--cache-to=type=registry,ref=${FULL_IMAGE}:buildcache,mode=max"
        output_type="registry"
    fi

    # Build and optionally push production image
    log_info "Building production image for platforms: $PLATFORMS"
    docker buildx build \
        --platform "$PLATFORMS" \
        --target production \
        -t "${FULL_IMAGE}:${TAG}" \
        -t "${FULL_IMAGE}:production" \
        -f src/docker/Dockerfile \
        ${cache_from} \
        ${cache_to} \
        $([ "$push" == "true" ] && echo "--push" || echo "--load") \
        .

    log_success "Production image built successfully"

    # Build and optionally push development image
    log_info "Building development image for platforms: $PLATFORMS"
    docker buildx build \
        --platform "$PLATFORMS" \
        --target development \
        -t "${FULL_IMAGE}:dev" \
        -t "${FULL_IMAGE}:development" \
        -f src/docker/Dockerfile \
        ${cache_from} \
        $([ "$push" == "true" ] && echo "--push" || echo "--load") \
        .

    log_success "Development image built successfully"
}

# Test built images
test_images() {
    log_header "Testing Built Images"

    cd "$PROJECT_ROOT"

    # Test production image
    log_info "Testing production image..."
    if docker run --rm --platform linux/amd64 "${FULL_IMAGE}:${TAG}" python3 --version; then
        log_success "Production image Python test passed"
    else
        log_error "Production image Python test failed"
        return 1
    fi

    if docker run --rm --platform linux/amd64 "${FULL_IMAGE}:${TAG}" pdflatex --version >/dev/null 2>&1; then
        log_success "Production image LaTeX test passed"
    else
        log_error "Production image LaTeX test failed"
        return 1
    fi

    # Test development image
    log_info "Testing development image..."
    if docker run --rm --platform linux/amd64 "${FULL_IMAGE}:dev" python3 --version; then
        log_success "Development image test passed"
    else
        log_error "Development image test failed"
        return 1
    fi

    log_success "All image tests passed"
}

# Login to registry
registry_login() {
    log_header "Registry Authentication"

    if [[ -n "${DOCKER_USERNAME}" && -n "${DOCKER_PASSWORD}" ]]; then
        log_info "Logging in to ${REGISTRY}..."
        echo "${DOCKER_PASSWORD}" | docker login "${REGISTRY}" -u "${DOCKER_USERNAME}" --password-stdin
        log_success "Successfully logged in to registry"
    elif [[ "$REGISTRY" == "docker.io" ]]; then
        log_warning "No credentials provided. Attempting to use existing Docker Hub authentication..."
        if ! docker system info | grep -q "Username:"; then
            log_error "Not logged in to Docker Hub. Please run 'docker login' or set DOCKER_USERNAME and DOCKER_PASSWORD"
            exit 1
        fi
    else
        log_warning "No credentials provided for custom registry. Assuming authentication is already handled."
    fi
}

# Push images to registry
push_images() {
    log_header "Pushing Images to Registry"

    registry_login

    log_info "Pushing production images..."
    docker buildx imagetools inspect "${FULL_IMAGE}:${TAG}" >/dev/null 2>&1 || {
        log_error "Production image not found in registry cache. Building and pushing..."
        build_multiarch true
        return
    }

    log_success "Images pushed successfully to ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}"

    # Show manifest information
    log_info "Image manifest information:"
    docker buildx imagetools inspect "${FULL_IMAGE}:${TAG}" | head -20
}

# Clean up builder and resources
cleanup_builder() {
    local builder_name="rxiv-maker-builder"

    log_header "Cleaning Up Build Resources"

    log_info "Removing buildx builder..."
    docker buildx rm "$builder_name" --force || true

    log_info "Pruning build cache..."
    docker buildx prune -f

    log_success "Cleanup completed"
}

# Show image information
show_info() {
    log_header "Image Information"

    echo
    log_info "Available Images:"
    docker images "${FULL_IMAGE}*" 2>/dev/null || echo "No local images found"

    echo
    log_info "Registry Information:"
    echo "Registry: ${REGISTRY}"
    echo "Namespace: ${NAMESPACE}"
    echo "Image Name: ${IMAGE_NAME}"
    echo "Full Reference: ${FULL_IMAGE}:${TAG}"
    echo "Platforms: ${PLATFORMS}"

    if command -v docker &> /dev/null && docker buildx ls | grep -q "rxiv-maker-builder"; then
        echo
        log_info "Builder Information:"
        docker buildx ls | grep -A5 -B5 "rxiv-maker-builder" || true
    fi
}

# Show help
show_help() {
    cat << EOF
${BOLD}${CYAN}RXiv-Maker Multi-Architecture Build Script${NC}

${BOLD}USAGE:${NC}
    $0 <command> [options]

${BOLD}COMMANDS:${NC}
    ${GREEN}setup${NC}           Setup multi-architecture builder
    ${GREEN}build${NC}           Build multi-architecture images locally
    ${GREEN}test${NC}            Test built images
    ${GREEN}push${NC}            Build and push images to registry
    ${GREEN}info${NC}            Show image and builder information
    ${GREEN}clean${NC}           Clean up builder and cache
    ${GREEN}all${NC}             Run setup, build, test, and push
    ${GREEN}help${NC}            Show this help message

${BOLD}ENVIRONMENT VARIABLES:${NC}
    ${CYAN}IMAGE_NAME${NC}       Image name (default: rxiv-maker)
    ${CYAN}REGISTRY${NC}         Registry URL (default: docker.io)
    ${CYAN}NAMESPACE${NC}        Registry namespace (default: current user)
    ${CYAN}PLATFORMS${NC}        Target platforms (default: linux/amd64,linux/arm64)
    ${CYAN}TAG${NC}              Image tag (default: latest)
    ${CYAN}DOCKER_USERNAME${NC}  Registry username for authentication
    ${CYAN}DOCKER_PASSWORD${NC}  Registry password for authentication

${BOLD}EXAMPLES:${NC}
    # Basic build
    $0 build

    # Build and push with custom settings
    IMAGE_NAME=my-rxiv NAMESPACE=myorg $0 push

    # Build for specific platforms
    PLATFORMS=linux/amd64,linux/arm64,linux/arm/v7 $0 build

    # Full workflow
    $0 all

    # Clean up everything
    $0 clean

${BOLD}REGISTRY AUTHENTICATION:${NC}
    • For Docker Hub: Use 'docker login' or set DOCKER_USERNAME/DOCKER_PASSWORD
    • For custom registries: Set DOCKER_USERNAME/DOCKER_PASSWORD environment variables
    • For cloud registries: Use cloud-specific authentication (gcloud, aws, etc.)

${BOLD}NOTES:${NC}
    • Requires Docker with Buildx support
    • Multi-architecture builds use QEMU emulation for cross-compilation
    • Images are optimized for production with minimal size
    • Registry cache is used to speed up subsequent builds

EOF
}

# =====================================
# Main Script Logic
# =====================================
main() {
    case "${1:-help}" in
        setup)
            check_dependencies
            setup_builder
            ;;
        build)
            check_dependencies
            setup_builder
            build_multiarch false
            ;;
        test)
            check_dependencies
            test_images
            ;;
        push)
            check_dependencies
            setup_builder
            build_multiarch true
            ;;
        info)
            show_info
            ;;
        clean)
            cleanup_builder
            ;;
        all)
            check_dependencies
            setup_builder
            build_multiarch true
            test_images
            log_success "Complete workflow finished successfully!"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            echo
            show_help
            exit 1
            ;;
    esac
}

# =====================================
# Script Entry Point
# =====================================
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
