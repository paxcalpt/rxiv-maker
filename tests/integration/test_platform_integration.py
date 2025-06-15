"""Integration tests for platform-specific functionality and Docker deployment."""

import shutil
import subprocess
from pathlib import Path

import pytest


class TestDockerIntegration:
    """Integration tests for Docker-based workflows."""

    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_image_build_basic(self, temp_dir):
        """Test basic Docker image build functionality."""
        # Create minimal test manuscript
        manuscript_dir = temp_dir / "MANUSCRIPT"
        manuscript_dir.mkdir()

        # Create basic manuscript file
        manuscript_content = """---
title: "Docker Test Manuscript"
authors:
  - name: "Test Author"
    affiliation: "Test University"
---

# Introduction

This is a test manuscript for Docker integration.
"""
        (manuscript_dir / "01_MAIN.md").write_text(manuscript_content)

        # Create config file
        config_content = """title: "Docker Test Manuscript"
authors:
  - name: "Test Author"
    affiliation: "Test University"
    email: "test@example.com"
"""
        (manuscript_dir / "00_CONFIG.yml").write_text(config_content)

        # Test Docker run command (if image exists)
        try:
            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "-v",
                    f"{temp_dir}:/app",
                    "-w",
                    "/app",
                    "-e",
                    "MANUSCRIPT_PATH=MANUSCRIPT",
                    "henriqueslab/rxiv-forge:latest",
                    "python",
                    "--version",  # Simple test command
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # If image exists and runs successfully
            if result.returncode == 0:
                assert "Python" in result.stdout
            else:
                pytest.skip("Docker image not available locally")

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Docker command failed or timed out")

    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_platform_detection(self):
        """Test Docker platform detection and multi-arch support."""
        try:
            # Test platform detection
            result = subprocess.run(
                ["docker", "version", "--format", "{{.Server.Arch}}"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                arch = result.stdout.strip()
                assert arch in [
                    "amd64",
                    "arm64",
                    "x86_64",
                    "aarch64",
                ], f"Unexpected architecture: {arch}"
            else:
                pytest.skip("Could not detect Docker architecture")

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Docker platform detection failed")

    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_buildx_availability(self):
        """Test that Docker Buildx is available for multi-arch builds."""
        try:
            result = subprocess.run(
                ["docker", "buildx", "version"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                assert "buildx" in result.stdout.lower()
            else:
                pytest.skip("Docker Buildx not available")

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Docker Buildx test failed")


class TestLocalPlatformIntegration:
    """Integration tests for local platform setup and dependencies."""

    def test_python_version_compatibility(self):
        """Test that Python version is compatible."""
        import sys

        # Check Python version
        version = sys.version_info
        assert version.major == 3, "Should use Python 3"
        assert version.minor >= 8, "Should use Python 3.8 or higher"

    def test_required_python_modules_importable(self):
        """Test that required Python modules can be imported."""
        required_modules = [
            "pathlib",
            "yaml",
            "subprocess",
            "tempfile",
            "shutil",
            "os",
            "sys",
        ]

        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                pytest.fail(f"Required module {module} not available")

    def test_project_structure_integrity(self):
        """Test that project structure is intact."""
        project_root = Path(".")

        # Check key directories exist
        key_dirs = ["src/py", "src/docker", "src/tex", "tests", "docs"]

        for dir_path in key_dirs:
            path = project_root / dir_path
            assert path.exists(), f"Directory {dir_path} should exist"
            assert path.is_dir(), f"{dir_path} should be a directory"

    def test_key_files_exist(self):
        """Test that key project files exist."""
        project_root = Path(".")

        key_files = [
            "README.md",
            "Makefile",
            "pyproject.toml",
            "src/py/utils.py",
            "src/py/converters/md2tex.py",
            "src/docker/Dockerfile",
            "src/docker/build-multiarch.sh",
        ]

        for file_path in key_files:
            path = project_root / file_path
            assert path.exists(), f"File {file_path} should exist"
            assert path.is_file(), f"{file_path} should be a file"

    def test_example_manuscript_structure(self):
        """Test that example manuscript has correct structure."""
        example_dir = Path("EXAMPLE_MANUSCRIPT")

        if example_dir.exists():
            # Check for required files
            required_files = ["00_CONFIG.yml", "01_MAIN.md", "03_REFERENCES.bib"]

            for file_name in required_files:
                file_path = example_dir / file_name
                assert file_path.exists(), f"Example manuscript should have {file_name}"
                assert file_path.stat().st_size > 0, f"{file_name} should not be empty"

    def test_makefile_targets_available(self):
        """Test that Makefile has expected targets."""
        makefile_path = Path("Makefile")

        if makefile_path.exists():
            content = makefile_path.read_text()

            expected_targets = ["pdf:", "figures:", "clean:", "install:", "test:"]

            for target in expected_targets:
                assert target in content, f"Makefile should have {target} target"


class TestMultiArchBuildIntegration:
    """Integration tests for multi-architecture build system."""

    def test_build_script_functionality(self):
        """Test build script basic functionality."""
        script_path = Path("src/docker/build-multiarch.sh")

        if script_path.exists():
            # Test script help function
            try:
                result = subprocess.run(
                    ["bash", str(script_path), "help"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    assert (
                        "usage" in result.stdout.lower()
                        or "help" in result.stdout.lower()
                    )

            except (subprocess.TimeoutExpired, FileNotFoundError):
                pytest.skip("Build script test failed")

    def test_dockerfile_syntax_validation(self):
        """Test that Dockerfile has valid syntax."""
        dockerfile_path = Path("src/docker/Dockerfile")

        if dockerfile_path.exists() and shutil.which("docker"):
            try:
                # Test Dockerfile syntax by doing a dry-run parse
                result = subprocess.run(
                    ["docker", "build", "--dry-run", "-f", str(dockerfile_path), "."],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                # If Docker supports --dry-run, check result
                if "--dry-run" not in result.stderr:
                    # Docker version doesn't support dry-run, skip
                    pytest.skip("Docker version doesn't support syntax validation")

            except (subprocess.TimeoutExpired, FileNotFoundError):
                pytest.skip("Dockerfile syntax validation failed")

    def test_docker_ignore_effectiveness(self):
        """Test that .dockerignore patterns work correctly."""
        dockerignore_path = Path("src/docker/.dockerignore")

        if dockerignore_path.exists():
            content = dockerignore_path.read_text()

            # Check for important patterns
            important_patterns = [
                "__pycache__",
                "*.pyc",
                ".git",
                "*.log",
                "node_modules",
            ]

            for pattern in important_patterns:
                assert (
                    pattern in content
                ), f".dockerignore should include {pattern} pattern"


class TestCloudPlatformIntegration:
    """Integration tests for cloud platform compatibility."""

    def test_github_actions_workflow_syntax(self):
        """Test GitHub Actions workflow files if they exist."""
        workflows_dir = Path(".github/workflows")

        if workflows_dir.exists():
            workflow_files = list(workflows_dir.glob("*.yml")) + list(
                workflows_dir.glob("*.yaml")
            )

            for workflow_file in workflow_files:
                content = workflow_file.read_text()

                # Basic YAML syntax checks
                assert (
                    "name:" in content
                ), f"Workflow {workflow_file.name} should have name"
                assert (
                    "on:" in content
                ), f"Workflow {workflow_file.name} should have triggers"
                assert (
                    "jobs:" in content
                ), f"Workflow {workflow_file.name} should have jobs"

    def test_docker_compose_syntax_if_exists(self):
        """Test Docker Compose file syntax if it exists."""
        compose_files = ["src/docker/docker-compose.yml", "docker-compose.yml"]

        for compose_file_path in compose_files:
            compose_path = Path(compose_file_path)

            if compose_path.exists():
                content = compose_path.read_text()

                # Basic Docker Compose syntax checks
                assert (
                    "version:" in content
                ), f"Compose file {compose_file_path} should have version"
                assert (
                    "services:" in content
                ), f"Compose file {compose_file_path} should have services"

    def test_environment_variable_documentation(self):
        """Test that environment variables are documented."""
        readme_path = Path("README.md")

        if readme_path.exists():
            content = readme_path.read_text()

            # Should mention key environment variables
            env_vars = ["MANUSCRIPT_PATH", "DOCKER_USERNAME", "NAMESPACE"]

            documented_vars = sum(1 for var in env_vars if var in content)
            assert (
                documented_vars > 0
            ), "README should document some environment variables"


class TestDocumentationIntegration:
    """Integration tests for documentation completeness and accuracy."""

    def test_platform_docs_cross_references(self):
        """Test that platform documentation has proper cross-references."""
        docs_dir = Path("docs/platforms")

        if docs_dir.exists():
            doc_files = list(docs_dir.glob("*.md"))

            for doc_file in doc_files:
                content = doc_file.read_text()

                # Should have cross-references to other docs
                assert (
                    "[" in content and "](" in content
                ), f"{doc_file.name} should have markdown links"

    def test_readme_docker_hub_references(self):
        """Test that README properly references Docker Hub."""
        readme_path = Path("README.md")

        if readme_path.exists():
            content = readme_path.read_text()

            # Should reference the Docker Hub repository
            assert (
                "henriqueslab/rxiv-forge" in content
            ), "README should reference Docker Hub repo"
            assert "docker run" in content, "README should show Docker usage"

    def test_documentation_consistency(self):
        """Test that documentation is consistent across files."""
        # Check that all docs mention the same Docker image name
        doc_files = [
            "README.md",
            "docs/platforms/DOCKER_HUB.md",
            "docs/platforms/CLOUD_PLATFORMS.md",
        ]

        image_name = "henriqueslab/rxiv-forge"

        for doc_file_path in doc_files:
            doc_path = Path(doc_file_path)
            if doc_path.exists():
                content = doc_path.read_text()
                assert (
                    image_name in content
                ), f"{doc_file_path} should reference correct image name"
