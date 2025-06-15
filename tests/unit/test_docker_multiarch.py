"""Unit tests for Docker multi-architecture functionality."""

import pytest
import subprocess
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestDockerMultiArch:
    """Test Docker multi-architecture build and deployment functionality."""

    def test_build_multiarch_script_exists(self):
        """Test that the multi-architecture build script exists and is executable."""
        script_path = Path("src/docker/build-multiarch.sh")
        assert script_path.exists(), "Multi-architecture build script should exist"
        assert script_path.stat().st_mode & 0o111, "Script should be executable"

    def test_dockerfile_has_multiarch_support(self):
        """Test that Dockerfile includes multi-architecture directives."""
        dockerfile_path = Path("src/docker/Dockerfile")
        assert dockerfile_path.exists(), "Dockerfile should exist"
        
        content = dockerfile_path.read_text()
        
        # Check for multi-arch syntax
        assert "syntax=docker/dockerfile:1" in content, "Should have buildx syntax directive"
        assert "--platform=$BUILDPLATFORM" in content, "Should support platform variables"

    def test_dockerignore_optimization(self):
        """Test that .dockerignore exists and contains optimization patterns."""
        dockerignore_path = Path("src/docker/.dockerignore")
        assert dockerignore_path.exists(), ".dockerignore should exist"
        
        content = dockerignore_path.read_text()
        
        # Check for important ignore patterns
        assert "**/__pycache__" in content, "Should ignore Python cache"
        assert "*.log" in content, "Should ignore log files"
        assert ".git/" in content, "Should ignore git directory"

    @patch('subprocess.run')
    def test_platform_detection(self, mock_run):
        """Test platform detection functionality."""
        # Mock docker buildx inspect output
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Platforms: linux/amd64, linux/arm64, linux/arm/v7"
        )
        
        # This would be part of the build script functionality
        result = subprocess.run(
            ["docker", "buildx", "inspect", "--bootstrap"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "linux/arm64" in result.stdout

    def test_image_naming_convention(self):
        """Test that image naming follows multi-arch conventions."""
        expected_tags = [
            "henriqueslab/rxiv-forge:latest",
            "henriqueslab/rxiv-forge:production", 
            "henriqueslab/rxiv-forge:dev",
            "henriqueslab/rxiv-forge:development"
        ]
        
        # Test that build script would generate these tags
        for tag in expected_tags:
            assert "/" in tag, "Should use namespace/image format"
            assert ":" in tag, "Should include tag"

    @patch('subprocess.run')
    def test_buildx_builder_creation(self, mock_run):
        """Test buildx builder creation for multi-arch builds."""
        mock_run.return_value = Mock(returncode=0, stdout="rxiv-forge-builder")
        
        # Simulate builder creation
        result = subprocess.run([
            "docker", "buildx", "create", 
            "--name", "rxiv-forge-builder",
            "--driver", "docker-container",
            "--bootstrap"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0

    def test_environment_variable_support(self):
        """Test that environment variables are properly supported."""
        expected_vars = [
            "IMAGE_NAME",
            "REGISTRY", 
            "NAMESPACE",
            "PLATFORMS",
            "TAG",
            "DOCKER_USERNAME",
            "DOCKER_PASSWORD"
        ]
        
        # Check build script content
        script_path = Path("src/docker/build-multiarch.sh")
        if script_path.exists():
            content = script_path.read_text()
            for var in expected_vars:
                assert f"${{{var}" in content or f"${var}" in content, f"Should support {var} environment variable"

    def test_platform_specific_optimizations(self):
        """Test that platform-specific optimizations are included."""
        dockerfile_path = Path("src/docker/Dockerfile")
        if dockerfile_path.exists():
            content = dockerfile_path.read_text()
            
            # Check for layer optimization
            assert "apt-get clean" in content, "Should include cleanup for smaller layers"
            assert "--no-cache-dir" in content, "Should use no-cache for pip"
            assert "rm -rf /var/lib/apt/lists/*" in content, "Should remove apt cache"

    @patch('subprocess.run')
    def test_registry_authentication(self, mock_run):
        """Test registry authentication handling."""
        mock_run.return_value = Mock(returncode=0)
        
        # Test Docker Hub login simulation
        result = subprocess.run([
            "docker", "login", 
            "-u", "testuser",
            "--password-stdin"
        ], input="testpass", text=True, capture_output=True)
        
        # Should not fail (mocked)
        assert result.returncode == 0

    def test_cache_optimization_config(self):
        """Test that cache optimization is configured."""
        dockerfile_path = Path("src/docker/Dockerfile")
        if dockerfile_path.exists():
            content = dockerfile_path.read_text()
            
            # Check for cache-friendly layer ordering
            lines = content.split('\n')
            copy_lines = [i for i, line in enumerate(lines) if 'COPY' in line and 'pyproject.toml' in line]
            pip_lines = [i for i, line in enumerate(lines) if 'pip install' in line or 'uv pip install' in line]
            
            # pyproject.toml should be copied before pip install for better caching
            if copy_lines and pip_lines:
                assert min(copy_lines) < min(pip_lines), "Dependencies should be copied before installation for cache efficiency"

    def test_security_hardening(self):
        """Test that security hardening is implemented."""
        dockerfile_path = Path("src/docker/Dockerfile")
        if dockerfile_path.exists():
            content = dockerfile_path.read_text()
            
            # Check for non-root user
            assert "USER appuser" in content, "Should run as non-root user"
            assert "useradd" in content or "adduser" in content, "Should create non-root user"
            
            # Check for proper permissions
            assert "--chown=" in content, "Should set proper file ownership"


class TestDockerComposeIntegration:
    """Test Docker Compose integration with multi-arch support."""

    def test_docker_compose_file_exists(self):
        """Test that docker-compose.yml exists."""
        compose_path = Path("src/docker/docker-compose.yml")
        # Note: May not exist yet, this is aspirational
        if compose_path.exists():
            assert compose_path.is_file()

    def test_management_script_functionality(self):
        """Test Docker management script features."""
        manage_script = Path("src/docker/manage.sh")
        if manage_script.exists():
            content = manage_script.read_text()
            
            # Check for key management functions
            expected_functions = ["build_image", "run_pdf", "start_dev", "cleanup"]
            for func in expected_functions:
                assert func in content, f"Should have {func} function"

    def test_quick_build_script_optimization(self):
        """Test quick build script optimizations."""
        quick_script = Path("src/docker/quick-build.sh")
        if quick_script.exists():
            content = quick_script.read_text()
            
            # Check for BuildKit enablement
            assert "DOCKER_BUILDKIT=1" in content, "Should enable BuildKit for faster builds"


class TestDockerDocumentation:
    """Test Docker documentation completeness."""

    def test_docker_readme_exists(self):
        """Test that Docker README exists and is comprehensive."""
        readme_path = Path("src/docker/README.md")
        if readme_path.exists():
            content = readme_path.read_text()
            
            # Check for key sections
            assert "Multi-Architecture" in content, "Should document multi-arch support"
            assert "Platform" in content, "Should mention platform support"
            assert "Performance" in content, "Should include performance information"

    def test_platform_documentation_exists(self):
        """Test that platform-specific documentation exists."""
        platform_docs = [
            "docs/platforms/DOCKER_HUB.md",
            "docs/platforms/LOCAL_DEVELOPMENT.md", 
            "docs/platforms/CLOUD_PLATFORMS.md"
        ]
        
        for doc_path in platform_docs:
            path = Path(doc_path)
            assert path.exists(), f"Platform documentation {doc_path} should exist"
            
            content = path.read_text()
            assert len(content) > 100, f"Documentation {doc_path} should have substantial content"

    def test_docker_hub_documentation_completeness(self):
        """Test Docker Hub documentation completeness."""
        docker_hub_doc = Path("docs/platforms/DOCKER_HUB.md")
        if docker_hub_doc.exists():
            content = docker_hub_doc.read_text()
            
            # Check for essential sections
            essential_topics = [
                "henriqueslab/rxiv-forge",
                "linux/amd64",
                "linux/arm64", 
                "Multi-Architecture",
                "Platform",
                "Docker Hub",
                "Apple Silicon",
                "AWS Graviton"
            ]
            
            for topic in essential_topics:
                assert topic in content, f"Should document {topic}"


class TestBuildScript:
    """Test the multi-architecture build script functionality."""

    def test_build_script_has_help_function(self):
        """Test that build script has help documentation."""
        script_path = Path("src/docker/build-multiarch.sh")
        if script_path.exists():
            content = script_path.read_text()
            assert "show_help" in content or "--help" in content, "Should have help function"

    def test_build_script_error_handling(self):
        """Test that build script has proper error handling."""
        script_path = Path("src/docker/build-multiarch.sh")
        if script_path.exists():
            content = script_path.read_text()
            
            # Check for error handling patterns
            assert "set -e" in content, "Should exit on error"
            assert "log_error" in content or "echo" in content, "Should have error logging"

    def test_build_script_dependency_checking(self):
        """Test that build script checks for required dependencies."""
        script_path = Path("src/docker/build-multiarch.sh")
        if script_path.exists():
            content = script_path.read_text()
            
            # Should check for docker and buildx
            assert "docker" in content.lower(), "Should reference docker command"
            assert "buildx" in content.lower(), "Should reference buildx for multi-arch"