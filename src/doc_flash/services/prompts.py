"""Prompt templates shared across providers."""


def build_documentation_prompt(code: str) -> str:
    """Ask the model to add docstrings and inline comments."""
    return (
        "You are a senior software engineer. "
        "Rewrite the snippet by adding concise docstrings and inline comments that explain intent, "
        "without altering behaviour or naming. "
        "Keep the original language and formatting style. "
        "Return only the updated code block.\n\n"
        "Code to document:\n"
        f"{code}"
    )


def build_markdown_prompt(code: str) -> str:
    """Ask the model to produce a markdown walkthrough."""
    return (
        "Summarise the following code into markdown aimed at developers. "
        "Include sections: Overview, Key Behaviours, Inputs/Outputs, Edge Cases, and Dependencies. "
        "Prefer bullet points, keep it brief, and avoid restating the full source code. "
        "Use fenced code snippets only when necessary for clarity.\n\n"
        "Code to analyse:\n"
        f"{code}"
    )


def build_tests_prompt(code: str) -> str:
    """Ask the model to suggest unit tests for the code."""
    return (
        "You are helping a developer add test coverage. "
        "Produce a set of unit tests for the code snippet below using pytest style. "
        "Focus on behaviour and edge cases, avoid over-mocking, and keep fixtures minimal. "
        "Return only the test code inside a single Python file.\n\n"
        "Code to test:\n"
        f"{code}"
    )
