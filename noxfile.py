# -*- coding: utf-8 -*-
import nox


@nox.session
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session
def tests(session):
    session.install(".[test]")
    session.run(
        "pytest",
        "--doctest-modules",
        "--cov=src/particle",
        "--cov-report=xml",
        *session.posargs
    )


@nox.session
def build(session):
    """
    Build an SDist and wheel.
    """

    session.install("build")
    session.run("python", "-m", "build")
