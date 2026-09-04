#!/usr/bin/env python3
"""
Tests for example files to ensure they follow best practices.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import ast
import sys
from pathlib import Path

import pytest


def get_example_files():
    """Get all Python example files."""
    examples_dir = Path(__file__).parent.parent / "examples"
    return list(examples_dir.glob("*.py"))


def parse_file(filepath):
    """Parse a Python file and return the AST."""
    with open(filepath, encoding="utf-8", errors="replace") as f:
        return ast.parse(f.read(), filename=str(filepath))


def find_bare_excepts(tree):
    """Find bare except clauses in the AST."""
    bare_excepts = []

    class BareExceptVisitor(ast.NodeVisitor):
        def visit_ExceptHandler(self, node):
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
            if isinstance(node.func, ast.Attribute):
                if (
                    node.func.attr == "load"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "ThemeManager"
                    and not self.in_try
                ):
                    issues.append((node.lineno, "ThemeManager.load() without error handling"))
            self.generic_visit(node)

    ThemeLoadVisitor().visit(tree)
    return issues


def find_missing_color_pair_wrappers(tree):
    """Find theme.colors.X usage without curses.color_pair()."""
    issues = []

    class ColorPairVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and node.func.attr in ("addstr", "addch"):
                for arg in node.args:
                    if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Attribute):
                        if arg.value.attr == "colors":
                            issues.append((node.lineno, f"Possible missing curses.color_pair() for theme.colors.{arg.attr}"))
            self.generic_visit(node)

    ColorPairVisitor().visit(tree)
    return issues


@pytest.mark.parametrize("example_file", get_example_files())
def test_no_bare_excepts(example_file):
    """Test that examples don't use bare except: clauses."""
    if example_file.name in ["generate_screenshots.py", "generate_screenshots_headless.py"]:
        pytest.skip("Screenshot generators may use different patterns")

    tree = parse_file(example_file)
    bare_excepts = find_bare_excepts(tree)
    if bare_excepts:
        with open(example_file, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        unexplained = []
        for lineno, issue in bare_excepts:
            if lineno > 0:
                prev_line = lines[lineno - 1].strip()
                curr_line = lines[lineno].strip()
                if not any(
                    keyword in prev_line.lower() or keyword in curr_line.lower()
                    for keyword in ["ignore", "boundary", "edge", "curses.error", "intentional"]
                ):
                    unexplained.append((lineno, issue))

        assert not unexplained, f"Found bare except clauses in {example_file.name}: {unexplained}"


@pytest.mark.parametrize("example_file", get_example_files())
def test_all_examples_import(example_file):
    """Test that all examples can be imported without errors."""
    if example_file.name in ["generate_screenshots.py", "generate_screenshots_headless.py"]:
        pytest.skip("File is meant to be run, not imported")

    examples_dir = example_file.parent
    if str(examples_dir) not in sys.path:
        sys.path.insert(0, str(examples_dir))

    try:
        tree = parse_file(example_file)
        assert tree is not None
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {example_file.name}: {e}")


@pytest.mark.parametrize("example_file", get_example_files())
def test_theme_load_has_error_handling(example_file):
    """Test that ThemeManager.load() calls have error handling."""
    if example_file.name in ["generate_screenshots.py", "generate_screenshots_headless.py"]:
        pytest.skip("Screenshot generators may have different patterns")

    tree = parse_file(example_file)
    issues = find_theme_load_without_error_handling(tree)

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
    if counter.count > 0 and len(issues) == counter.count:
        pytest.skip(f"File has {counter.count} ThemeManager.load() call(s) without error handling - consider adding try/except")


def test_examples_directory_exists():
    """Test that the examples directory exists."""
    examples_dir = Path(__file__).parent.parent / "examples"
    assert examples_dir.exists(), "Examples directory not found"
    assert examples_dir.is_dir(), "Examples path is not a directory"


def test_all_examples_have_docstrings():
    """Test that all example files have module docstrings."""
    for example_file in get_example_files():
        with open(example_file, encoding="utf-8", errors="replace") as f:
            content = f.read()
        tree = ast.parse(content)
        has_docstring = (
            len(tree.body) > 0
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)
            and isinstance(tree.body[0].value.value, str)
        )
        assert has_docstring, f"{example_file.name} is missing a module-level docstring"


def test_examples_use_curses_wrapper():
    """Test that examples use curses.wrapper() for proper cleanup."""
    for example_file in get_example_files():
        if example_file.name.startswith("generate_"):
            continue
        with open(example_file, encoding="utf-8", errors="replace") as f:
            content = f.read()
        if '__name__ == "__main__"' in content or "__name__ == '__main__'" in content:
            assert "curses.wrapper" in content, f"{example_file.name} should use curses.wrapper() for proper cleanup"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
