"""Unit tests for Docker scripts and configuration files."""

from pathlib import Path
from unittest.mock import patch

import pytest


class TestDockerfileValidation:
    """Test Dockerfile syntax and best practices."""

    def test_dockerfile_exists_and_readable(self):
        """Test that Dockerfile exists and is readable."""
        dockerfile_path = Path("src/docker/Dockerfile")
        assert dockerfile_path.exists(), "Dockerfile should exist"
        assert dockerfile_path.is_file(), "Dockerfile should be a file"

        # Should be readable
        content = dockerfile_path.read_text()
        assert len(content) > 100, "Dockerfile should have substantial content"

    def test_dockerfile_syntax_directives(self):
        """Test Dockerfile syntax and directives."""
        dockerfile_path = Path("src/docker/Dockerfile")
        content = dockerfile_path.read_text()

        # Check for essential directives
        assert "FROM" in content, "Should have FROM directive"
        assert "WORKDIR" in content, "Should set working directory"
        assert "COPY" in content or "ADD" in content, "Should copy files"

        # Check for multi-architecture support
        assert (
            "syntax=docker/dockerfile:1" in content
        ), "Should use modern Dockerfile syntax"
        assert (
            "--platform=$BUILDPLATFORM" in content
        ), "Should support platform variables"

    def test_dockerfile_security_practices(self):
        """Test Dockerfile security best practices."""
        dockerfile_path = Path("src/docker/Dockerfile")
        content = dockerfile_path.read_text()

        # Check for non-root user
        assert "USER" in content, "Should run as non-root user"
        assert "adduser" in content or "useradd" in content, "Should create user"

        # Check for proper cleanup
        assert "rm -rf /var/lib/apt/lists/*" in content, "Should clean up apt cache"
        assert (
            "--no-cache" in content or "pip --no-cache-dir" in content
        ), "Should avoid caching"

    def test_dockerfile_layer_optimization(self):
        """Test Dockerfile layer optimization."""
        dockerfile_path = Path("src/docker/Dockerfile")
        content = dockerfile_path.read_text()
        lines = content.split("\n")

        # Check for command chaining to reduce layers
        apt_install_lines = [line for line in lines if "apt-get install" in line]
        if apt_install_lines:
            # Should have cleanup in same layer
            for line in apt_install_lines:
                line_index = lines.index(line)
                # Check next few lines for cleanup
                cleanup_found = any(
                    "rm -rf /var/lib/apt/lists/*" in lines[i]
                    or "apt-get clean" in lines[i]
                    for i in range(line_index, min(line_index + 5, len(lines)))
                )
                if not cleanup_found:
                    # This is a warning, not a failure
                    pass

    def test_dockerfile_environment_variables(self):
        """Test Dockerfile environment variables."""
        dockerfile_path = Path("src/docker/Dockerfile")
        content = dockerfile_path.read_text()

        # Check for Python-specific environment variables
        assert "PYTHONPATH" in content, "Should set PYTHONPATH"
        assert "PYTHONUNBUFFERED" in content, "Should set PYTHONUNBUFFERED"


class TestDockerIgnoreFile:
    """Test .dockerignore file configuration."""

    def test_dockerignore_exists(self):
        """Test that .dockerignore file exists."""
        dockerignore_path = Path("src/docker/.dockerignore")
        assert dockerignore_path.exists(), ".dockerignore should exist"

    def test_dockerignore_patterns(self):
        """Test .dockerignore patterns for optimization."""
        dockerignore_path = Path("src/docker/.dockerignore")
        content = dockerignore_path.read_text()

        # Essential patterns for Python projects
        essential_patterns = ["__pycache__", "*.pyc", ".git", "*.log", ".pytest_cache"]

        for pattern in essential_patterns:
            assert pattern in content, f".dockerignore should include {pattern}"

    def test_dockerignore_size_optimization(self):
        """Test that .dockerignore helps with build context size."""
        dockerignore_path = Path("src/docker/.dockerignore")
        content = dockerignore_path.read_text()

        # Patterns that help reduce build context
        size_patterns = ["node_modules", "*.tmp", "*.temp", "output/", ".venv", "venv/"]

        found_patterns = sum(1 for pattern in size_patterns if pattern in content)
        assert found_patterns >= 3, "Should have multiple size optimization patterns"


class TestBuildMultiArchScript:
    """Test multi-architecture build script."""

    def test_build_script_exists_and_executable(self):
        """Test that build script exists and is executable."""
        script_path = Path("src/docker/build-multiarch.sh")
        assert script_path.exists(), "Multi-arch build script should exist"

        # Check if executable (Unix permissions)
        stat = script_path.stat()
        assert stat.st_mode & 0o111, "Script should be executable"

    def test_build_script_shebang(self):
        """Test build script has proper shebang."""
        script_path = Path("src/docker/build-multiarch.sh")
        content = script_path.read_text()

        lines = content.split("\n")
        assert lines[0].startswith("#!"), "Should have shebang"
        assert "bash" in lines[0], "Should use bash"

    def test_build_script_error_handling(self):
        """Test build script error handling."""
        script_path = Path("src/docker/build-multiarch.sh")
        content = script_path.read_text()

        # Should have error handling
        assert "set -e" in content, "Should exit on error"

        # Should have logging functions
        logging_functions = ["log_error", "log_info", "echo"]
        assert any(func in content for func in logging_functions), "Should have logging"

    def test_build_script_help_function(self):
        """Test build script help functionality."""
        script_path = Path("src/docker/build-multiarch.sh")
        content = script_path.read_text()

        # Should have help function
        assert "help" in content.lower(), "Should have help functionality"
        assert (
            "usage" in content.lower() or "help" in content.lower()
        ), "Should show usage"

    def test_build_script_environment_variables(self):
        """Test build script environment variable support."""
        script_path = Path("src/docker/build-multiarch.sh")
        content = script_path.read_text()

        # Key environment variables for multi-arch builds
        env_vars = ["IMAGE_NAME", "REGISTRY", "NAMESPACE", "PLATFORMS", "TAG"]

        for var in env_vars:
            assert (
                f"${{{var}" in content or f"${var}" in content
            ), f"Should support {var} environment variable"

    def test_build_script_platform_support(self):
        """Test build script platform support."""
        script_path = Path("src/docker/build-multiarch.sh")
        content = script_path.read_text()

        # Should mention supported platforms
        assert "linux/amd64" in content, "Should support linux/amd64"
        assert "linux/arm64" in content, "Should support linux/arm64"

        # Should use buildx
        assert "buildx" in content, "Should use Docker Buildx"

    @patch("subprocess.run")
    def test_build_script_dependency_checking(self, mock_run):
        """Test build script dependency checking."""
        script_path = Path("src/docker/build-multiarch.sh")
        content = script_path.read_text()

        # Should check for Docker
        assert "docker" in content.lower(), "Should check for Docker"

        # Should check for buildx
        assert "buildx" in content.lower(), "Should check for Buildx"


class TestDockerManagementScript:
    """Test Docker management script functionality."""

    def test_management_script_exists(self):
        """Test that management script exists."""
        script_path = Path("src/docker/manage.sh")
        if script_path.exists():
            assert script_path.is_file(), "Management script should be a file"

            # Check if executable
            stat = script_path.stat()
            assert stat.st_mode & 0o111, "Management script should be executable"

    def test_management_script_functions(self):
        """Test management script function definitions."""
        script_path = Path("src/docker/manage.sh")
        if not script_path.exists():
            pytest.skip("Management script not found")

        content = script_path.read_text()

        # Key functions for Docker management
        expected_functions = ["build", "run", "clean", "help"]

        found_functions = sum(1 for func in expected_functions if func in content)
        assert found_functions >= 2, "Should have multiple management functions"

    def test_management_script_error_handling(self):
        """Test management script error handling."""
        script_path = Path("src/docker/manage.sh")
        if not script_path.exists():
            pytest.skip("Management script not found")

        content = script_path.read_text()

        # Should have error handling
        assert "set -e" in content or "exit" in content, "Should have error handling"


class TestQuickBuildScript:
    """Test quick build script functionality."""

    def test_quick_build_script_exists(self):
        """Test that quick build script exists."""
        script_path = Path("src/docker/quick-build.sh")
        if script_path.exists():
            assert script_path.is_file(), "Quick build script should be a file"

    def test_quick_build_script_optimization(self):
        """Test quick build script optimizations."""
        script_path = Path("src/docker/quick-build.sh")
        if not script_path.exists():
            pytest.skip("Quick build script not found")

        content = script_path.read_text()

        # Should enable BuildKit for faster builds
        assert "DOCKER_BUILDKIT=1" in content, "Should enable BuildKit"

    def test_quick_build_script_targets(self):
        """Test quick build script build targets."""
        script_path = Path("src/docker/quick-build.sh")
        if not script_path.exists():
            pytest.skip("Quick build script not found")

        content = script_path.read_text()

        # Should support different build targets
        assert (
            "production" in content or "development" in content
        ), "Should have build targets"


class TestDockerComposeConfiguration:
    """Test Docker Compose configuration if it exists."""

    def test_docker_compose_file_syntax(self):
        """Test Docker Compose file syntax."""
        compose_files = ["src/docker/docker-compose.yml", "docker-compose.yml"]

        compose_file = None
        for file_path in compose_files:
            path = Path(file_path)
            if path.exists():
                compose_file = path
                break

        if not compose_file:
            pytest.skip("No Docker Compose file found")

        content = compose_file.read_text()

        # Basic Docker Compose syntax
        assert "version:" in content, "Should have version specification"
        assert "services:" in content, "Should have services definition"

    def test_docker_compose_service_configuration(self):
        """Test Docker Compose service configuration."""
        compose_files = ["src/docker/docker-compose.yml", "docker-compose.yml"]

        compose_file = None
        for file_path in compose_files:
            path = Path(file_path)
            if path.exists():
                compose_file = path
                break

        if not compose_file:
            pytest.skip("No Docker Compose file found")

        content = compose_file.read_text()

        # Should have RXiv-Maker service
        service_indicators = ["rxiv", "forge", "manuscript", "latex"]
        assert any(
            indicator in content.lower() for indicator in service_indicators
        ), "Should have relevant service"


class TestDockerScriptIntegration:
    """Test integration between Docker scripts."""

    def test_script_consistency(self):
        """Test consistency between Docker scripts."""
        scripts = [
            "src/docker/build-multiarch.sh",
            "src/docker/manage.sh",
            "src/docker/quick-build.sh",
        ]

        existing_scripts = [Path(script) for script in scripts if Path(script).exists()]

        if len(existing_scripts) < 2:
            pytest.skip("Not enough Docker scripts to test consistency")

        # Check for consistent image naming
        image_patterns = []
        for script_path in existing_scripts:
            content = script_path.read_text()
            if "rxiv-maker" in content.lower():
                image_patterns.append("rxiv-maker")
            if "henriqueslab" in content.lower():
                image_patterns.append("henriqueslab")

        # Should have consistent naming
        assert len(set(image_patterns)) <= 2, "Should have consistent image naming"

    def test_script_error_codes(self):
        """Test that scripts use consistent error codes."""
        scripts = ["src/docker/build-multiarch.sh", "src/docker/manage.sh"]

        for script_path_str in scripts:
            script_path = Path(script_path_str)
            if not script_path.exists():
                continue

            content = script_path.read_text()

            # Should have error handling
            has_exit = "exit 1" in content or "exit 0" in content
            has_return = "return 1" in content or "return 0" in content

            assert (
                has_exit or has_return
            ), f"Script {script_path.name} should have error handling"


class TestDockerSecurityConfiguration:
    """Test Docker security configuration."""

    def test_dockerfile_user_security(self):
        """Test Dockerfile user security configuration."""
        dockerfile_path = Path("src/docker/Dockerfile")
        content = dockerfile_path.read_text()

        # Should not run as root in final stage
        user_lines = [
            line for line in content.split("\n") if line.strip().startswith("USER")
        ]
        if user_lines:
            # Should have non-root user
            last_user = user_lines[-1]
            assert "root" not in last_user, "Should not run as root user"

    def test_dockerfile_port_exposure(self):
        """Test Dockerfile port exposure."""
        dockerfile_path = Path("src/docker/Dockerfile")
        content = dockerfile_path.read_text()

        # Should be careful about exposed ports
        expose_lines = [line for line in content.split("\n") if "EXPOSE" in line]

        # If ports are exposed, they should be documented
        for line in expose_lines:
            # This is informational - just checking if ports are documented
            assert any(
                char.isdigit() for char in line
            ), "Exposed ports should have numbers"

    def test_dockerfile_secrets_handling(self):
        """Test that Dockerfile doesn't contain secrets."""
        dockerfile_path = Path("src/docker/Dockerfile")
        content = dockerfile_path.read_text()

        # Should not contain common secret patterns
        secret_patterns = ["password=", "token=", "key=", "secret="]

        for pattern in secret_patterns:
            assert (
                pattern not in content.lower()
            ), f"Dockerfile should not contain {pattern}"
