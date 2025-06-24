"""Nox configuration for RXiv-Maker testing."""

import nox


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def tests(session):
    """Run the test suite."""
    # Install dependencies with explicit versions to avoid conflicts
    session.install(".")
    session.install("pytest>=7.4,<8.0", "py>=1.11.0", "pytest-cov>=4.0")
    session.install("ruff>=0.8.0", "mypy>=1.0", "pytest-notebook>=0.10.0")
    session.install("lazydocs>=0.4.8", "nbstripout>=0.7.1", "pre-commit>=4.0.0")
    session.run("pytest", "tests/", "-v")


@nox.session(venv_backend="none")
def tests_current(session):
    """Run tests in current Python environment (no virtualenv)."""
    session.run("pytest", "tests/", "-v")


@nox.session(python="3.11")
def lint(session):
    """Run linting checks."""
    session.install(".[dev]")
    session.run("ruff", "check", "src/")
    session.run("ruff", "format", "--check", "src/")


@nox.session(python="3.11")
def type_check(session):
    """Run type checking."""
    session.install(".")
    session.install("mypy>=1.0", "types-PyYAML>=6.0.0")
    session.run("mypy", "src/")


@nox.session(python="3.11")
def format(session):
    """Format code with ruff."""
    session.install(".[dev]")
    session.run("ruff", "format", "src/")


@nox.session(python="3.11")
def integration(session):
    """Run integration tests that generate actual PDFs."""
    session.install(".")
    session.install("pytest>=7.4,<8.0", "py>=1.11.0", "pytest-cov>=4.0")
    session.install("pytest-notebook>=0.10.0")
    session.run("pytest", "tests/integration/", "-v", "-s")


@nox.session(python="3.11")
def coverage(session):
    """Run tests with coverage reporting."""
    session.install(".")
    session.install("pytest>=7.4,<8.0", "py>=1.11.0")
    session.install("coverage[toml]>=7.0", "pytest-cov>=4.0")
    session.install("pytest-notebook>=0.10.0")
    session.run(
        "pytest",
        "tests/",
        "--cov=src/py",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v",
    )
