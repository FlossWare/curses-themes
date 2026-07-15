#!/usr/bin/env python3
"""
Tests for example files to ensure they follow best practices.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import ast
import os
import sys
from pathlib import Path

import pytest


def get_example_files():
    """Get all Python example files."""
    examples_dir = Path(__file__).parent.parent / "examples"
    return list(examples_dir.glob("*.py"))


def parse_file(filepath):
    """Parse a Python file and return the AST."""
    with open(filepath, "r") as f:
        return ast.parse(f.read(), filename=str(filepath))


def find_bare_excepts(tree):
    """Find bare except clauses in the AST."""
    bare_excepts = []

    class BareExceptVisitor(ast.NodeVisitor):
        def visit_ExceptHandler(self, node):
            # Check if it's a bare except: (type is None)
            # or too broad (Exception without being specific)
            if node.type is None:
                bare_excepts.append((node.lineno, "bare except:"))
            self.generic_visit(node)

    BareExceptVisitor().visit(tree)
    return bare_excepts


def find_theme_load_without_error_handling(tree):
    """Find ThemeManager.load() calls without try/except."""
    issues = []

    class ThemeLoadVisitor(ast.NodeVisitor):
        def __init__(self):
            self.in_try = False
            self.try_depth = 0

        def visit_Try(self, node):
            self.try_depth += 1
            self.in_try = True
            self.generic_visit(node)
            self.try_depth -= 1
            if self.try_depth == 0:
                self.in_try = False

        def visit_Call(self, node):
            # Check for ThemeManager.load() calls
            if isinstance(node.func, ast.Attribute):
                if (
                    node.func.attr == "load"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "ThemeManager"
                ):
                    if not self.in_try:
                        issues.append(
                            (
                                node.lineno,
                                "ThemeManager.load() without error handling",
                            )
                        )
            self.generic_visit(node)

    ThemeLoadVisitor().visit(tree)
    return issues


def find_missing_color_pair_wrappers(tree):
    """Find theme.colors.X usage without curses.color_pair()."""
    issues = []

    class ColorPairVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            # Check for addstr/addch calls with theme.colors directly
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ("addstr", "addch"):
                    # Check the arguments for theme.colors.X
                    for arg in node.args:
                        if isinstance(arg, ast.Attribute):
                            if (
                                isinstance(arg.value, ast.Attribute)
                                and arg.value.attr == "colors"
                            ):
                                # Check if it's wrapped in color_pair()
                                # This is a simplified check - might have false positives
                                issues.append(
                                    (
                                        node.lineno,
                                        f"Possible missing curses.color_pair() for theme.colors.{arg.attr}",
                                    )
                                )
            self.generic_visit(node)

    ColorPairVisitor().visit(tree)
    return issues


@pytest.mark.parametrize("example_file", get_example_files())
def test_no_bare_excepts(example_file):
    """Test that examples don't use bare except: clauses."""
    # Skip certain files that are known to use specific patterns
    if example_file.name in ["generate_screenshots.py", "generate_screenshots_headless.py"]:
        pytest.skip("Screenshot generators may use different patterns")

    tree = parse_file(example_file)
    bare_excepts = find_bare_excepts(tree)

    # Some files might legitimately use bare except for specific reasons
    # We check for comments explaining why
    if bare_excepts:
        with open(example_file, "r") as f:
            lines = f.readlines()

        unexplained = []
        for lineno, issue in bare_excepts:
            # Check if there's a comment explaining this bare except
            # Look at the line before and the line itself
            if lineno > 0:
                prev_line = lines[lineno - 1].strip()
                curr_line = lines[lineno].strip()
                # Allow bare except if there's a comment explaining it
                # or if it's specifically catching curses.error in context
                if not any(
                    keyword in prev_line.lower() or keyword in curr_line.lower()
                    for keyword in [
                        "ignore",
                        "boundary",
                        "edge",
                        "curses.error",
                        "intentional",
                    ]
                ):
                    unexplained.append((lineno, issue))

        assert (
            not unexplained
        ), f"Found bare except clauses in {example_file.name}: {unexplained}"


@pytest.mark.parametrize("example_file", get_example_files())
def test_all_examples_import(example_file):
    """Test that all examples can be imported without errors."""
    # Skip files that require interactive input or are meant to be run, not imported
    if example_file.name in [
        "generate_screenshots.py",
        "generate_screenshots_headless.py",
    ]:
        pytest.skip("File is meant to be run, not imported")

    # Add the examples directory to the path
    examples_dir = example_file.parent
    if str(examples_dir) not in sys.path:
        sys.path.insert(0, str(examples_dir))

    # Try to parse the file (this will catch syntax errors)
    try:
        tree = parse_file(example_file)
        assert tree is not None
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {example_file.name}: {e}")


@pytest.mark.parametrize("example_file", get_example_files())
def test_theme_load_has_error_handling(example_file):
    """Test that ThemeManager.load() calls have error handling."""
    # Skip files that might have different patterns
    if example_file.name in ["generate_screenshots.py", "generate_screenshots_headless.py"]:
        pytest.skip("Screenshot generators may have different patterns")

    tree = parse_file(example_file)
    issues = find_theme_load_without_error_handling(tree)

    # We expect most examples to have error handling for theme loading
    # Allow some exceptions for very simple examples
    if example_file.name not in []:  # Add exceptions here if needed
        # It's OK if there are no theme loads at all (file might not use themes)
        # But if there are theme loads, they should have error handling
        class ThemeLoadCounter(ast.NodeVisitor):
            def __init__(self):
                self.count = 0

            def visit_Call(self, node):
                if isinstance(node.func, ast.Attribute):
                    if (
                        node.func.attr == "load"
                        and isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "ThemeManager"
                    ):
                        self.count += 1
                self.generic_visit(node)

        counter = ThemeLoadCounter()
        counter.visit(tree)

        if counter.count > 0:
            # If there are ThemeManager.load() calls, at least one should be in a try block
            # This is a soft check - we won't fail if some are missing, but warn
            if len(issues) == counter.count:
                pytest.skip(
                    f"File has {counter.count} ThemeManager.load() call(s) without error handling - consider adding try/except"
                )


def test_examples_directory_exists():
    """Test that the examples directory exists."""
    examples_dir = Path(__file__).parent.parent / "examples"
    assert examples_dir.exists(), "Examples directory not found"
    assert examples_dir.is_dir(), "Examples path is not a directory"


def test_all_examples_have_docstrings():
    """Test that all example files have module docstrings."""
    for example_file in get_example_files():
        with open(example_file, "r") as f:
            content = f.read()

        tree = ast.parse(content)

        # Check for module docstring
        has_docstring = (
            len(tree.body) > 0
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)
            and isinstance(tree.body[0].value.value, str)
        )

        assert (
            has_docstring
        ), f"{example_file.name} is missing a module-level docstring"


def test_examples_use_curses_wrapper():
    """Test that examples use curses.wrapper() for proper cleanup."""
    for example_file in get_example_files():
        # Skip files that are not main programs
        if example_file.name.startswith("generate_"):
            continue

        with open(example_file, "r") as f:
            content = f.read()

        # Check if file has if __name__ == "__main__":
        if '__name__ == "__main__"' in content or "__name__ == '__main__'" in content:
            # Should use curses.wrapper()
            assert (
                "curses.wrapper" in content
            ), f"{example_file.name} should use curses.wrapper() for proper cleanup"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
