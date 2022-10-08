from __future__ import annotations

from pathlib import Path

import nox

nox.options.sessions = ["lint", "pylint", "tests"]


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session
def pylint(session: nox.Session) -> None:
    """
    Run pylint.
    """

    session.install("pylint~=2.15.0")
    session.install("-e", ".[dev]")
    session.run("pylint", "src", *session.posargs)


@nox.session
def tests(session: nox.Session) -> None:
    session.install("-e", ".[test]")
    session.run(
        "pytest",
        *session.posargs,
    )


@nox.session
def build(session: nox.Session) -> None:
    """
    Build an SDist and wheel.
    """

    session.install("build", "twine", "check-wheel-contents")
    session.run("python", "-m", "build")
    session.run("twine", "check", "--strict", "dist/*")
    session.run(
        "check-wheel-contents", str(*Path("dist").glob("*.whl")), "--ignore=W002"
    )


@nox.session
def zipapp(session: nox.Session) -> None:
    tmpdir = session.create_tmp()

    # Build a distribution
    session.run(
        "python",
        "-m",
        "pip",
        "install",
        ".",
        "attrs",
        "hepunits",
        "importlib_resources",
        "deprecated",
        f"--target={tmpdir}",
    )

    # Build the zipapp out of the local directory
    outfile = Path("particle.pyz").resolve()
    session.chdir(tmpdir)
    session.run(
        "python",
        "-m",
        "zipapp",
        "--compress",
        "--python=/usr/bin/env python3",
        "--main=particle.__main__:main",
        f"--output={outfile}",
        ".",
    )

    # Quick test to verify it works
    session.chdir(str(outfile.parent))
    result = session.run("python", "particle.pyz", "search", "D0", silent=True)
    if "Name: D0" not in result:
        session.error(
            f"Expected valid result, was unable to run zipapp. Produced: {result}"
        )
