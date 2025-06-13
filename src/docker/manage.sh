#!/bin/bash
# RXiv-Forge Docker Management Script
# Consolidated script for all Docker operations with optimized builds

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
DOCKER_DIR="${SCRIPT_DIR}"

# Docker configuration
COMPOSE_FILE="${DOCKER_DIR}/docker-compose.yml"
DOCKERFILE="${DOCKER_DIR}/Dockerfile"
IMAGE_NAME="rxiv-forge"

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
    
    if ! command -v docker &> /dev/null || ! docker compose version &> /dev/null 2>&1; then
        if ! command -v docker-compose &> /dev/null; then
            log_error "Docker Compose is not available"
            echo "Please install Docker Compose"
            exit 1
        else
            COMPOSE_CMD="docker-compose"
        fi
    else
        COMPOSE_CMD="docker compose"
    fi
    
    log_success "Dependencies check passed"
}

# Determine compose command
get_compose_cmd() {
    if command -v docker-compose &> /dev/null; then
        echo "docker-compose"
    else
        echo "docker compose"
    fi
}

# =====================================
# Build Functions
# =====================================
build_image() {
    local target="${1:-production}"
    local no_cache="${2:-false}"
    
    log_header "Building RXiv-Forge Docker Image (${target})"
    
    cd "$PROJECT_ROOT"
    
    local build_args=""
    if [[ "$no_cache" == "true" ]]; then
        build_args="--no-cache"
    fi
    
    # Enable BuildKit for better performance
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    
    local compose_cmd=$(get_compose_cmd)
    
    log_info "Building ${target} image..."
    if $compose_cmd -f "$COMPOSE_FILE" build $build_args --build-arg BUILDKIT_INLINE_CACHE=1 rxiv-forge; then
        log_success "Docker image built successfully"
        
        # Also build dev image if building production
        if [[ "$target" == "production" ]]; then
            log_info "Building development image..."
            $compose_cmd -f "$COMPOSE_FILE" build $build_args dev
            log_success "Development image built successfully"
        fi
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

# =====================================
# Service Management Functions
# =====================================
run_pdf() {
    log_header "Generating PDF with RXiv-Forge"
    
    cd "$PROJECT_ROOT"
    local compose_cmd=$(get_compose_cmd)
    
    # Check if image exists
    if ! docker images "${IMAGE_NAME}" | grep -q "${IMAGE_NAME}"; then
        log_warning "Docker image not found. Building..."
        build_image "production"
    fi
    
    log_info "Running PDF generation..."
    if $compose_cmd -f "$COMPOSE_FILE" run --rm rxiv-forge make pdf; then
        log_success "PDF generated successfully"
        log_info "Output available in: ${PROJECT_ROOT}/output/"
    else
        log_error "PDF generation failed"
        exit 1
    fi
}

start_dev() {
    log_header "Starting Development Environment"
    
    cd "$PROJECT_ROOT"
    local compose_cmd=$(get_compose_cmd)
    
    # Build dev image if it doesn't exist
    if ! docker images "${IMAGE_NAME}:dev" | grep -q "${IMAGE_NAME}"; then
        log_warning "Development image not found. Building..."
        build_image "development"
    fi
    
    log_info "Starting development container..."
    $compose_cmd -f "$COMPOSE_FILE" up -d dev
    log_success "Development environment started"
    log_info "Access shell with: $0 shell"
}

start_watch() {
    log_header "Starting Watch Mode"
    
    cd "$PROJECT_ROOT"
    local compose_cmd=$(get_compose_cmd)
    
    log_info "Starting watch mode..."
    $compose_cmd -f "$COMPOSE_FILE" up watch
}

open_shell() {
    log_header "Opening Interactive Shell"
    
    cd "$PROJECT_ROOT"
    local compose_cmd=$(get_compose_cmd)
    
    # Check if dev container is running
    if ! $compose_cmd -f "$COMPOSE_FILE" ps dev | grep -q "Up"; then
        log_info "Starting development container..."
        start_dev
        sleep 2
    fi
    
    log_info "Opening shell in development container..."
    $compose_cmd -f "$COMPOSE_FILE" exec dev bash
}

run_tests() {
    log_header "Running Tests"
    
    cd "$PROJECT_ROOT"
    local compose_cmd=$(get_compose_cmd)
    
    log_info "Running tests in container..."
    $compose_cmd -f "$COMPOSE_FILE" --profile testing run --rm test
}

stop_all() {
    log_header "Stopping All Services"
    
    cd "$PROJECT_ROOT"
    local compose_cmd=$(get_compose_cmd)
    
    log_info "Stopping all containers..."
    $compose_cmd -f "$COMPOSE_FILE" down
    log_success "All services stopped"
}

cleanup() {
    log_header "Cleaning Up Docker Resources"
    
    cd "$PROJECT_ROOT"
    local compose_cmd=$(get_compose_cmd)
    
    log_info "Stopping and removing containers..."
    $compose_cmd -f "$COMPOSE_FILE" down --volumes --remove-orphans
    
    log_info "Removing images..."
    docker images "${IMAGE_NAME}*" -q | xargs -r docker rmi -f
    
    log_info "Cleaning up unused resources..."
    docker system prune -f
    
    log_success "Cleanup completed"
}

show_status() {
    log_header "Docker Service Status"
    
    cd "$PROJECT_ROOT"
    local compose_cmd=$(get_compose_cmd)
    
    echo
    log_info "Container Status:"
    $compose_cmd -f "$COMPOSE_FILE" ps
    
    echo
    log_info "Image Information:"
    docker images "${IMAGE_NAME}*"
    
    echo
    log_info "Volume Usage:"
    docker volume ls | grep "rxiv-forge" || echo "No volumes found"
}

# =====================================
# Help and Usage
# =====================================
show_help() {
    cat << EOF
${BOLD}${CYAN}RXiv-Forge Docker Management Script${NC}

${BOLD}USAGE:${NC}
    $0 <command> [options]

${BOLD}COMMANDS:${NC}
    ${GREEN}build${NC} [target] [--no-cache]  Build Docker image
                                 target: production (default) | development
    ${GREEN}pdf${NC}                         Generate PDF using Docker
    ${GREEN}dev${NC}                         Start development environment
    ${GREEN}watch${NC}                       Start watch mode (auto-rebuild)
    ${GREEN}shell${NC}                       Open interactive shell in dev container
    ${GREEN}test${NC}                        Run tests in container
    ${GREEN}stop${NC}                        Stop all running services
    ${GREEN}restart${NC}                     Restart all services
    ${GREEN}status${NC}                      Show service and image status
    ${GREEN}clean${NC}                       Clean up all Docker resources
    ${GREEN}help${NC}                        Show this help message

${BOLD}EXAMPLES:${NC}
    $0 build                    # Build production image
    $0 build development        # Build development image
    $0 build --no-cache         # Build without cache
    $0 pdf                      # Generate PDF
    $0 dev                      # Start development environment
    $0 shell                    # Open shell in development container
    $0 watch                    # Start file watching for auto-rebuild
    $0 clean                    # Clean up everything

${BOLD}CONFIGURATION:${NC}
    Docker Compose: ${COMPOSE_FILE}
    Dockerfile:     ${DOCKERFILE}
    Project Root:   ${PROJECT_ROOT}

${BOLD}OPTIMIZATION FEATURES:${NC}
    • Multi-stage Docker builds for minimal image size
    • BuildKit support for faster builds and caching
    • Separated volumes for cache and development persistence
    • Resource limits to prevent system overload
    • Security hardening with non-root user
    • Efficient layer caching strategy

EOF
}

# =====================================
# Main Script Logic
# =====================================
main() {
    # Change to project root
    cd "$PROJECT_ROOT"
    
    # Check dependencies first
    check_dependencies
    
    # Parse command line arguments
    case "${1:-help}" in
        build)
            target="${2:-production}"
            no_cache="false"
            if [[ "$2" == "--no-cache" ]] || [[ "$3" == "--no-cache" ]]; then
                no_cache="true"
            fi
            build_image "$target" "$no_cache"
            ;;
        pdf)
            run_pdf
            ;;
        dev)
            start_dev
            ;;
        watch)
            start_watch
            ;;
        shell)
            open_shell
            ;;
        test)
            run_tests
            ;;
        stop)
            stop_all
            ;;
        restart)
            stop_all
            sleep 2
            start_dev
            ;;
        status)
            show_status
            ;;
        clean)
            cleanup
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
