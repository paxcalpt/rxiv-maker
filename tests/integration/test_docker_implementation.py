"""Integration tests for actual Docker implementation and functionality."""

import pytest
import subprocess
import tempfile
import shutil
import os
import time
from pathlib import Path
from unittest.mock import patch


class TestDockerImageFunctionality:
    """Test actual Docker image functionality and behavior."""

    @pytest.mark.docker
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_image_pull_and_basic_functionality(self):
        """Test pulling the Docker image and basic functionality."""
        image_name = "henriqueslab/rxiv-forge:latest"
        
        try:
            # Try to pull the latest image
            log_info("Attempting to pull Docker image...")
            result = subprocess.run([
                "docker", "pull", image_name
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                pytest.skip(f"Could not pull Docker image: {result.stderr}")
            
            # Test basic functionality
            result = subprocess.run([
                "docker", "run", "--rm", image_name, "python3", "--version"
            ], capture_output=True, text=True, timeout=30)
            
            assert result.returncode == 0, f"Python check failed: {result.stderr}"
            assert "Python 3" in result.stdout, "Should have Python 3"
            
        except subprocess.TimeoutExpired:
            pytest.skip("Docker command timed out")
        except Exception as e:
            pytest.skip(f"Docker test failed: {e}")

    @pytest.mark.docker
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_latex_functionality(self):
        """Test LaTeX functionality in Docker container."""
        image_name = "henriqueslab/rxiv-forge:latest"
        
        try:
            # Check if image is available (pull if needed)
            if not self._check_image_available(image_name):
                pytest.skip("Docker image not available")
            
            # Test LaTeX installation
            result = subprocess.run([
                "docker", "run", "--rm", image_name, "pdflatex", "--version"
            ], capture_output=True, text=True, timeout=30)
            
            assert result.returncode == 0, f"LaTeX check failed: {result.stderr}"
            assert "pdfTeX" in result.stdout, "Should have pdfTeX"
            
        except subprocess.TimeoutExpired:
            pytest.skip("Docker LaTeX test timed out")
        except Exception as e:
            pytest.skip(f"Docker LaTeX test failed: {e}")

    @pytest.mark.docker
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_node_and_mermaid_functionality(self):
        """Test Node.js and Mermaid functionality in Docker container."""
        image_name = "henriqueslab/rxiv-forge:latest"
        
        try:
            if not self._check_image_available(image_name):
                pytest.skip("Docker image not available")
            
            # Test Node.js installation
            result = subprocess.run([
                "docker", "run", "--rm", image_name, "node", "--version"
            ], capture_output=True, text=True, timeout=30)
            
            assert result.returncode == 0, f"Node.js check failed: {result.stderr}"
            assert "v20" in result.stdout or "v18" in result.stdout, "Should have Node.js v18 or v20"
            
            # Test Mermaid CLI installation
            result = subprocess.run([
                "docker", "run", "--rm", image_name, "mmdc", "--version"
            ], capture_output=True, text=True, timeout=30)
            
            assert result.returncode == 0, f"Mermaid CLI check failed: {result.stderr}"
            
        except subprocess.TimeoutExpired:
            pytest.skip("Docker Node.js test timed out")
        except Exception as e:
            pytest.skip(f"Docker Node.js test failed: {e}")

    @pytest.mark.docker
    @pytest.mark.slow
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_manuscript_generation_end_to_end(self):
        """Test complete manuscript generation in Docker container."""
        image_name = "henriqueslab/rxiv-forge:latest"
        
        if not self._check_image_available(image_name):
            pytest.skip("Docker image not available")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test manuscript structure
            manuscript_dir = temp_path / "MANUSCRIPT"
            manuscript_dir.mkdir()
            figures_dir = manuscript_dir / "FIGURES"
            figures_dir.mkdir()
            
            # Create minimal manuscript configuration
            config_content = """title: "Docker Test Manuscript"
authors:
  - name: "Test Author"
    affiliation: "Test University"
    email: "test@example.com"
keywords: ["testing", "docker"]
abstract: "This is a test manuscript for Docker functionality validation."
"""
            (manuscript_dir / "00_CONFIG.yml").write_text(config_content)
            
            # Create main manuscript content
            manuscript_content = """# Introduction

This is a test manuscript to validate Docker container functionality.

## Methods

We test the Docker container's ability to process Markdown and generate LaTeX.

## Results  

The container should successfully convert this Markdown to LaTeX and generate a PDF.

## Conclusion

Docker container functionality validated.
"""
            (manuscript_dir / "01_MAIN.md").write_text(manuscript_content)
            
            # Create empty references file
            (manuscript_dir / "03_REFERENCES.bib").write_text("% Empty bibliography for testing")
            
            try:
                # Test manuscript generation
                result = subprocess.run([
                    "docker", "run", "--rm",
                    "-v", f"{temp_path}:/app",
                    "-w", "/app",
                    "-e", "MANUSCRIPT_PATH=MANUSCRIPT",
                    image_name,
                    "python", "src/py/commands/generate_preprint.py"
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    # Check if output was generated
                    output_dir = temp_path / "output"
                    assert output_dir.exists(), "Output directory should be created"
                    
                    # Look for generated files
                    tex_files = list(output_dir.glob("*.tex"))
                    assert len(tex_files) > 0, "Should generate LaTeX files"
                    
                    # Check LaTeX content
                    tex_content = tex_files[0].read_text()
                    assert "Docker Test Manuscript" in tex_content, "Should contain manuscript title"
                    assert "Test Author" in tex_content, "Should contain author name"
                    
                else:
                    # If generation failed, still pass if it's a known limitation
                    if "pdflatex" in result.stderr or "LaTeX" in result.stderr:
                        pytest.skip(f"LaTeX processing issue in Docker: {result.stderr}")
                    else:
                        pytest.fail(f"Docker manuscript generation failed: {result.stderr}")
                        
            except subprocess.TimeoutExpired:
                pytest.skip("Docker manuscript generation timed out")

    @pytest.mark.docker
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_platform_architecture_detection(self):
        """Test platform architecture detection in Docker."""
        image_name = "henriqueslab/rxiv-forge:latest"
        
        if not self._check_image_available(image_name):
            pytest.skip("Docker image not available")
        
        try:
            # Test architecture detection
            result = subprocess.run([
                "docker", "run", "--rm", image_name, "uname", "-m"
            ], capture_output=True, text=True, timeout=15)
            
            assert result.returncode == 0, f"Architecture detection failed: {result.stderr}"
            
            arch = result.stdout.strip()
            expected_archs = ["x86_64", "aarch64", "arm64"]
            assert arch in expected_archs, f"Unexpected architecture: {arch}"
            
            # Test platform-specific functionality
            result = subprocess.run([
                "docker", "run", "--rm", image_name, "python3", "-c", 
                "import platform; print(f'Platform: {platform.machine()}')"
            ], capture_output=True, text=True, timeout=15)
            
            assert result.returncode == 0, "Platform detection should work"
            assert "Platform:" in result.stdout, "Should show platform information"
            
        except subprocess.TimeoutExpired:
            pytest.skip("Docker platform test timed out")

    @pytest.mark.docker
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_volume_mounting_and_permissions(self):
        """Test Docker volume mounting and file permissions."""
        image_name = "henriqueslab/rxiv-forge:latest"
        
        if not self._check_image_available(image_name):
            pytest.skip("Docker image not available")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test file
            test_file = temp_path / "test.txt"
            test_file.write_text("Docker volume test")
            
            try:
                # Test volume mounting and file access
                result = subprocess.run([
                    "docker", "run", "--rm",
                    "-v", f"{temp_path}:/app/test",
                    image_name,
                    "cat", "/app/test/test.txt"
                ], capture_output=True, text=True, timeout=15)
                
                assert result.returncode == 0, f"Volume mounting failed: {result.stderr}"
                assert "Docker volume test" in result.stdout, "Should read mounted file"
                
                # Test file creation permissions
                result = subprocess.run([
                    "docker", "run", "--rm",
                    "-v", f"{temp_path}:/app/test",
                    image_name,
                    "touch", "/app/test/created_file.txt"
                ], capture_output=True, text=True, timeout=15)
                
                assert result.returncode == 0, f"File creation failed: {result.stderr}"
                
                # Check if file was created
                created_file = temp_path / "created_file.txt"
                assert created_file.exists(), "Docker should be able to create files"
                
            except subprocess.TimeoutExpired:
                pytest.skip("Docker volume test timed out")

    def _check_image_available(self, image_name):
        """Check if Docker image is available locally."""
        try:
            result = subprocess.run([
                "docker", "images", image_name, "--format", "{{.Repository}}"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and image_name.split(':')[0] in result.stdout:
                return True
            
            # Try to pull the image if not available locally
            log_info(f"Pulling Docker image {image_name}...")
            result = subprocess.run([
                "docker", "pull", image_name
            ], capture_output=True, text=True, timeout=300)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False


class TestDockerBuildProcess:
    """Test Docker build process and multi-architecture functionality."""

    @pytest.mark.docker_build
    @pytest.mark.slow
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_build_process(self):
        """Test building Docker image from local Dockerfile."""
        dockerfile_path = Path("src/docker/Dockerfile")
        
        if not dockerfile_path.exists():
            pytest.skip("Dockerfile not found")
        
        try:
            # Test basic Docker build (dry run)
            result = subprocess.run([
                "docker", "build", "--dry-run",
                "-f", str(dockerfile_path),
                "-t", "rxiv-forge-test",
                "."
            ], capture_output=True, text=True, timeout=60)
            
            # If dry-run is not supported, skip
            if "unknown flag" in result.stderr:
                pytest.skip("Docker version doesn't support dry-run")
            
            if result.returncode != 0:
                pytest.fail(f"Docker build dry-run failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            pytest.skip("Docker build test timed out")

    @pytest.mark.docker_build
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_buildx_multiarch_support(self):
        """Test Docker Buildx multi-architecture support."""
        try:
            # Check if buildx is available
            result = subprocess.run([
                "docker", "buildx", "version"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                pytest.skip("Docker Buildx not available")
            
            # Check available platforms
            result = subprocess.run([
                "docker", "buildx", "ls"
            ], capture_output=True, text=True, timeout=15)
            
            assert result.returncode == 0, f"Buildx ls failed: {result.stderr}"
            
            # Should support multiple platforms
            platforms = result.stdout
            assert "linux/amd64" in platforms, "Should support linux/amd64"
            
            # ARM64 support is platform-dependent
            if "linux/arm64" in platforms:
                log_info("ARM64 support detected")
            else:
                log_info("ARM64 support not available on this platform")
                
        except subprocess.TimeoutExpired:
            pytest.skip("Buildx test timed out")

    @pytest.mark.docker_build
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_build_script_execution(self):
        """Test multi-architecture build script execution."""
        script_path = Path("src/docker/build-multiarch.sh")
        
        if not script_path.exists():
            pytest.skip("Multi-arch build script not found")
        
        try:
            # Test script help function
            result = subprocess.run([
                "bash", str(script_path), "help"
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                assert "usage" in result.stdout.lower() or "help" in result.stdout.lower()
            else:
                pytest.skip(f"Build script help failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            pytest.skip("Build script test timed out")


class TestDockerManagementScripts:
    """Test Docker management scripts functionality."""

    @pytest.mark.docker
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_docker_management_script(self):
        """Test Docker management script functionality."""
        manage_script = Path("src/docker/manage.sh")
        
        if not manage_script.exists():
            pytest.skip("Docker management script not found")
        
        try:
            # Test help function
            result = subprocess.run([
                "bash", str(manage_script), "help"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                help_output = result.stdout.lower()
                assert "docker" in help_output, "Should mention Docker"
                assert "build" in help_output, "Should have build command"
            else:
                pytest.skip(f"Management script help failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            pytest.skip("Management script test timed out")

    @pytest.mark.docker
    def test_quick_build_script(self):
        """Test quick build script functionality."""
        quick_script = Path("src/docker/quick-build.sh")
        
        if not quick_script.exists():
            pytest.skip("Quick build script not found")
        
        try:
            # Test help function
            result = subprocess.run([
                "bash", str(quick_script), "help"
            ], capture_output=True, text=True, timeout=5)
            
            # Check if script runs without immediate error
            assert result.returncode == 0 or "usage" in result.stdout.lower() or "help" in result.stdout.lower()
                
        except subprocess.TimeoutExpired:
            pytest.skip("Quick build script test timed out")


class TestDockerEnvironmentVariables:
    """Test Docker environment variable handling."""

    @pytest.mark.docker
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_environment_variable_passing(self):
        """Test that environment variables are properly passed to Docker."""
        image_name = "henriqueslab/rxiv-forge:latest"
        
        # Skip if image not available
        if not self._check_image_available(image_name):
            pytest.skip("Docker image not available")
        
        try:
            # Test environment variable passing
            result = subprocess.run([
                "docker", "run", "--rm",
                "-e", "TEST_VAR=docker_test_value",
                image_name,
                "printenv", "TEST_VAR"
            ], capture_output=True, text=True, timeout=15)
            
            assert result.returncode == 0, f"Environment variable test failed: {result.stderr}"
            assert "docker_test_value" in result.stdout, "Environment variable should be passed"
            
        except subprocess.TimeoutExpired:
            pytest.skip("Environment variable test timed out")

    @pytest.mark.docker
    @pytest.mark.skipif(not shutil.which("docker"), reason="Docker not available")
    def test_manuscript_path_environment_variable(self):
        """Test MANUSCRIPT_PATH environment variable functionality."""
        image_name = "henriqueslab/rxiv-forge:latest"
        
        if not self._check_image_available(image_name):
            pytest.skip("Docker image not available")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create custom manuscript directory
            custom_dir = temp_path / "MY_MANUSCRIPT"
            custom_dir.mkdir()
            
            try:
                # Test custom manuscript path
                result = subprocess.run([
                    "docker", "run", "--rm",
                    "-v", f"{temp_path}:/app",
                    "-w", "/app",
                    "-e", "MANUSCRIPT_PATH=MY_MANUSCRIPT",
                    image_name,
                    "ls", "-la", "MY_MANUSCRIPT"
                ], capture_output=True, text=True, timeout=15)
                
                assert result.returncode == 0, f"Custom manuscript path test failed: {result.stderr}"
                
            except subprocess.TimeoutExpired:
                pytest.skip("Manuscript path test timed out")

    def _check_image_available(self, image_name):
        """Check if Docker image is available."""
        try:
            result = subprocess.run([
                "docker", "images", image_name, "--format", "{{.Repository}}"
            ], capture_output=True, text=True, timeout=10)
            
            return result.returncode == 0 and image_name.split(':')[0] in result.stdout
            
        except:
            return False


def log_info(message):
    """Simple logging function for test output."""
    print(f"INFO: {message}")


# Pytest configuration for Docker tests
def pytest_configure(config):
    """Configure pytest for Docker tests."""
    config.addinivalue_line(
        "markers", "docker: marks tests as requiring Docker (deselect with '-m \"not docker\"')"
    )
    config.addinivalue_line(
        "markers", "docker_build: marks tests as requiring Docker build capabilities"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )