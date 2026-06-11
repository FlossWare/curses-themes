# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in curses-themes, please report it responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please report security issues privately via:

1. **GitHub Security Advisories** (preferred)
   - Go to: https://github.com/FlossWare/curses-themes/security/advisories
   - Click "Report a vulnerability"
   - Fill out the form with details

2. **Email** (if GitHub is unavailable)
   - Contact the project maintainers through GitHub
   - Subject: "[SECURITY] Brief description"
   - Include: Detailed description, steps to reproduce, impact assessment

### What to Include

A good security report includes:

- **Description** - What is the vulnerability?
- **Impact** - What can an attacker do with this vulnerability?
- **Affected versions** - Which versions are vulnerable?
- **Steps to reproduce** - How can we verify the vulnerability?
- **Proof of concept** - Example code showing the vulnerability (if applicable)
- **Suggested fix** - Ideas for how to fix it (optional)

### Response Timeline

- **24 hours** - We will acknowledge receipt of your report
- **5 business days** - We will provide an initial assessment
- **30 days** - We aim to release a patch or mitigation

### Disclosure Policy

- We follow **coordinated disclosure**
- We will work with you to understand and fix the issue
- We will credit you in the release notes (unless you prefer anonymity)
- We ask that you do not publicly disclose the vulnerability until we've released a fix

### Scope

This security policy applies to:

- **curses-themes library code** (curses_themes/*.py)
- **Themes** (curses_themes/themes/*.py)
- **Examples** (examples/*.py) if they demonstrate insecure patterns

Out of scope:

- Third-party dependencies (report to those projects directly)
- Social engineering attacks
- Physical security issues

## Security Best Practices

When using curses-themes:

1. **Sanitize user input** - Themes render text but don't validate it
2. **Limit theme loading** - Only load themes from trusted sources
3. **Terminal escape sequences** - Be aware themes use ANSI/curses escape codes
4. **Resource limits** - Large color maps can consume memory

## Hall of Fame

We recognize security researchers who responsibly disclose vulnerabilities:

- *Your name could be here!*

## Questions?

For non-security questions, please open a regular GitHub issue or discussion.
For security concerns, use the private reporting methods above.
