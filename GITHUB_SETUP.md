# GitHub Repository Setup Guide

## Repository Topics/Tags

Add these topics to your GitHub repository for better discoverability:

### Primary Topics
```
python
curses
terminal
tui
themes
theming
terminal-ui
```

### Technology Topics
```
python3
ncurses
terminal-colors
color-schemes
```

### Feature Topics
```
retro-computing
vintage-themes
terminal-themes
tui-framework
dark-mode
light-mode
```

### Specific Themes
```
dos
dbase
ti-99-4a
trs-80
borland
```

### How to Add Topics

1. Go to your repository page on GitHub
2. Click the ⚙️ (gear) icon next to "About"
3. In the "Topics" field, add the topics above (comma-separated)
4. Click "Save changes"

Or via GitHub CLI:
```bash
gh repo edit FlossWare/curses-themes --add-topic "python,curses,terminal,tui,themes,terminal-ui,retro-computing,ncurses"
```

## Repository Description

**Suggested description:**
```
Lightweight theme support for Python curses applications with 8 built-in themes including retro computer and classic software themes. Zero dependencies.
```

## Repository Settings

### Enable Features
- ✅ Issues
- ✅ Projects (optional)
- ✅ Wiki (optional for additional docs)
- ✅ Discussions (for community Q&A)

### Branch Protection
Protect `main` branch:
- Require pull request reviews
- Require status checks to pass
- Require conversation resolution

### About Section
- Website: (Add documentation URL when deployed)
- Topics: (See list above)
- Description: (See suggested description)
- Add social preview image (create screenshot of theme gallery)

## Labels

Create these issue labels:

### Type Labels
- `bug` - Something isn't working (red)
- `feature` - New feature request (green)
- `documentation` - Documentation improvements (blue)
- `theme` - New theme or theme improvements (purple)
- `enhancement` - Enhancement to existing feature (cyan)

### Priority Labels
- `priority: high` - High priority issue (red)
- `priority: medium` - Medium priority (orange)
- `priority: low` - Low priority (yellow)

### Status Labels
- `good first issue` - Good for newcomers (green)
- `help wanted` - Extra attention needed (yellow)
- `wontfix` - This will not be worked on (gray)

### Platform Labels
- `windows` - Windows-specific issue
- `linux` - Linux-specific issue
- `macos` - macOS-specific issue

## GitHub Actions (Suggested)

Create `.github/workflows/test.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest --cov=curses_themes tests/
```

## README Badges

Add these badges to your README.md:

```markdown
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/curses-themes.svg)](https://badge.fury.io/py/curses-themes)
[![Tests](https://github.com/FlossWare/curses-themes/workflows/Tests/badge.svg)](https://github.com/FlossWare/curses-themes/actions)
[![Documentation Status](https://readthedocs.org/projects/curses-themes/badge/?version=latest)](https://curses-themes.readthedocs.io/en/latest/?badge=latest)
```

## Social Preview Image

Create a 1280x640px image showing:
- Library name and tagline
- Side-by-side screenshots of 3-4 themes
- Python logo and terminal icon
- "8 Built-in Themes" callout

Upload in Settings → Options → Social preview

## Links to Add

In your README, link to:
- Documentation (GUIDE.md, API.md)
- Examples directory
- Contributing guidelines
- curses-java (inspiration credit)
- Issue tracker
- Discussions

## Community Files

Create `.github/` directory with:
- `ISSUE_TEMPLATE/bug_report.md`
- `ISSUE_TEMPLATE/feature_request.md`
- `ISSUE_TEMPLATE/theme_submission.md`
- `PULL_REQUEST_TEMPLATE.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`

## PyPI Publishing

When ready to publish:

1. Create `setup.py` or use `pyproject.toml`
2. Build package: `python -m build`
3. Upload to PyPI: `python -m twine upload dist/*`
4. Update README with PyPI installation instructions

## Documentation Hosting

Options:
- **Read the Docs** - Auto-builds from markdown
- **GitHub Pages** - Host static docs
- **GitHub Wiki** - Collaborative documentation

## Checklist

- [ ] Add repository topics
- [ ] Update repository description
- [ ] Enable Issues, Discussions
- [ ] Create issue labels
- [ ] Add README badges
- [ ] Create social preview image
- [ ] Set up GitHub Actions
- [ ] Add issue templates
- [ ] Add SECURITY.md
- [ ] Configure branch protection
- [ ] Link to documentation
- [ ] Credit curses-java inspiration
