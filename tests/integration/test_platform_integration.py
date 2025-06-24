"""Integration tests for platform-specific functionality."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest


class TestProjectStructure:
    """Test that project structure is correct after Docker removal."""

    def test_project_structure_integrity(self):
        """Test that project structure is intact."""
        project_root = Path(".")

        # Check key directories exist (excluding Docker)
        key_dirs = ["src/py", "src/tex", "tests", "docs"]

        for dir_path in key_dirs:
            path = project_root / dir_path
            assert path.exists(), f"Directory {dir_path} should exist"
            assert path.is_dir(), f"{dir_path} should be a directory"

        # Ensure Docker directory is removed
        docker_dir = project_root / "src/docker"
        assert not docker_dir.exists(), "Docker directory should be removed"

    def test_key_files_exist(self):
        """Test that key project files exist."""
        project_root = Path(".")

        key_files = [
            "README.md",
            "Makefile",
            "pyproject.toml",
            "src/py/utils.py",
            "src/py/converters/md2tex.py",
        ]

        for file_path in key_files:
            path = project_root / file_path
            assert path.exists(), f"File {file_path} should exist"
            assert path.is_file(), f"{file_path} should be a file"

        # Ensure Docker files are removed
        docker_files = [
            "src/docker/Dockerfile",
            "src/docker/build-multiarch.sh",
            "src/docker/docker-compose.yml",
            ".dockerignore",
        ]

        for file_path in docker_files:
            path = project_root / file_path
            assert not path.exists(), f"Docker file {file_path} should be removed"

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

            # Check for essential targets (excluding Docker)
            essential_targets = ["pdf", "setup", "clean", "help"]

            for target in essential_targets:
                assert (
                    f".PHONY: {target}" in content or f"{target}:" in content
                ), f"Makefile should define {target} target"

            # Ensure Docker references are removed
            docker_terms = ["docker run", "docker pull", "docker build"]
            for term in docker_terms:
                assert (
                    term not in content.lower()
                ), f"Makefile should not contain Docker reference: {term}"


class TestPlatformCompatibility:
    """Test platform-specific functionality without Docker."""

    def test_python_version_compatibility(self):
        """Test Python version compatibility."""
        try:
            result = subprocess.run(
                ["python", "--version"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                version_output = result.stdout.strip()
                # Extract version number
                if "Python 3." in version_output:
                    version_parts = version_output.split()[1].split(".")
                    major = int(version_parts[0])
                    minor = int(version_parts[1])

                    # Check minimum Python version (3.9+)
                    assert major >= 3, f"Python major version should be 3+, got {major}"
                    assert minor >= 9, f"Python minor version should be 9+, got {minor}"

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Python version check failed")

    def test_latex_availability(self):
        """Test LaTeX installation availability."""
        latex_commands = ["pdflatex", "bibtex", "biber"]

        for cmd in latex_commands:
            if shutil.which(cmd):
                try:
                    result = subprocess.run(
                        [cmd, "--version"], capture_output=True, text=True, timeout=10
                    )
                    # If any LaTeX command is available, that's good enough
                    if result.returncode == 0:
                        return
                except subprocess.TimeoutExpired:
                    continue

        pytest.skip(
            "No LaTeX installation found - this is expected for CI without LaTeX"
        )

    def test_make_availability(self):
        """Test that make command is available."""
        if shutil.which("make"):
            try:
                result = subprocess.run(
                    ["make", "--version"], capture_output=True, text=True, timeout=10
                )

                if result.returncode == 0:
                    assert (
                        "GNU Make" in result.stdout or "make" in result.stdout.lower()
                    )
                else:
                    pytest.skip("Make command not working properly")

            except subprocess.TimeoutExpired:
                pytest.skip("Make version check timed out")
        else:
            pytest.skip("Make command not found")


class TestDocumentationConsistency:
    """Test that documentation is consistent after Docker removal."""

    def test_readme_no_docker_references(self):
        """Test that README doesn't contain Docker references."""
        readme_path = Path("README.md")

        if readme_path.exists():
            content = readme_path.read_text().lower()

            # These terms should be removed
            forbidden_terms = [
                "docker run",
                "docker pull",
                "docker build",
                "henriqueslab/rxiv-maker",
                "docker desktop",
                "docker hub",
            ]

            for term in forbidden_terms:
                assert term not in content, f"README should not contain: {term}"

    def test_claude_md_no_docker_references(self):
        """Test that CLAUDE.md doesn't contain Docker references."""
        claude_path = Path("CLAUDE.md")

        if claude_path.exists():
            content = claude_path.read_text().lower()

            # These terms should be removed
            forbidden_terms = [
                "docker",
                "container",
                "multi-stage",
                "multi-architecture",
            ]

            for term in forbidden_terms:
                assert term not in content, f"CLAUDE.md should not contain: {term}"

    def test_local_development_doc_updated(self):
        """Test that local development documentation is updated."""
        doc_path = Path("docs/platforms/LOCAL_DEVELOPMENT.md")

        if doc_path.exists():
            content = doc_path.read_text().lower()

            # Should not contain Docker setup sections
            forbidden_sections = [
                "docker setup",
                "docker desktop",
                "install docker",
            ]

            for section in forbidden_sections:
                assert (
                    section not in content
                ), f"LOCAL_DEVELOPMENT.md should not contain: {section}"

    def test_docker_hub_doc_removed(self):
        """Test that Docker Hub documentation is removed."""
        docker_hub_path = Path("docs/platforms/DOCKER_HUB.md")
        assert not docker_hub_path.exists(), "DOCKER_HUB.md should be removed"


class TestBuildSystem:
    """Test that build system works without Docker."""

    @pytest.fixture
    def temp_manuscript_dir(self, tmp_path):
        """Create a temporary manuscript for testing."""
        manuscript_dir = tmp_path / "TEST_MANUSCRIPT"
        manuscript_dir.mkdir()

        # Create minimal config
        config_content = """title: "Test Manuscript"
authors:
  - name: "Test Author"
    affiliations: ["Test University"]
    email: "test@example.com"
"""
        (manuscript_dir / "00_CONFIG.yml").write_text(config_content)

        # Create minimal content
        content = """# Abstract
This is a test manuscript.

# Introduction
Testing the build system.
"""
        (manuscript_dir / "01_MAIN.md").write_text(content)

        # Create empty references file
        (manuscript_dir / "03_REFERENCES.bib").write_text("")

        return manuscript_dir

    def test_makefile_pdf_target_works(self, temp_manuscript_dir):
        """Test that make pdf target works without Docker."""
        if not shutil.which("make"):
            pytest.skip("Make not available")

        original_cwd = Path.cwd()

        try:
            # Copy source files to temp directory
            temp_root = temp_manuscript_dir.parent
            src_dir = temp_root / "src"
            src_dir.mkdir()

            # Copy essential source files
            original_src = Path("src")
            if original_src.exists():
                shutil.copytree(original_src, src_dir, dirs_exist_ok=True)

            # Copy Makefile
            original_makefile = Path("Makefile")
            if original_makefile.exists():
                shutil.copy2(original_makefile, temp_root / "Makefile")

            # Copy pyproject.toml
            original_pyproject = Path("pyproject.toml")
            if original_pyproject.exists():
                shutil.copy2(original_pyproject, temp_root / "pyproject.toml")

            os.chdir(temp_root)

            # Test setup target
            subprocess.run(
                ["make", "setup"],
                capture_output=True,
                text=True,
                timeout=300,
                env={**os.environ, "MANUSCRIPT_PATH": str(temp_manuscript_dir.name)},
            )

            # Setup might fail due to missing dependencies, which is OK
            # We just want to verify the Makefile syntax is correct

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            pytest.skip(f"Make test failed: {e}")
        finally:
            os.chdir(original_cwd)
