"""Nox configuration for RXiv-Maker testing."""

import nox


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def tests(session):
    """Run the test suite."""
    session.install(".[dev]")
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
    session.install(".[dev]")
    session.run("mypy", "src/")


@nox.session(python="3.11")
def format(session):
    """Format code with ruff."""
    session.install(".[dev]")
    session.run("ruff", "format", "src/")


@nox.session(python="3.11")
def integration(session):
    """Run integration tests that generate actual PDFs."""
    session.install(".[dev]")
    session.run("pytest", "tests/integration/", "-v", "-s")


@nox.session(python="3.11")
def coverage(session):
    """Run tests with coverage reporting."""
    session.install(".[dev]", "coverage[toml]", "pytest-cov")
    session.run(
        "pytest",
        "tests/",
        "--cov=src/py",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v",
    )
