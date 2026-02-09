# Security Policy

## Supported Versions

We actively support the following versions of REAPER with security updates:

| Version | Supported          | Status      |
| ------- | ------------------ | ----------- |
| 0.1.x   | :white_check_mark: | Development |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in REAPER, please follow these steps:

### 1. **DO NOT** Open a Public Issue

Security vulnerabilities should not be publicly disclosed until they have been addressed.

### 2. Report Privately

Please report security vulnerabilities through one of these channels:

- **Preferred:** Use GitHub's [Security Advisories](https://github.com/SaltProphet/Reaper/security/advisories/new) feature
- **Alternative:** Email the maintainers directly (see repository settings for contact)

### 3. Include Details

When reporting a vulnerability, please include:

- **Description:** Clear description of the vulnerability
- **Impact:** What could an attacker achieve?
- **Steps to Reproduce:** Detailed steps to reproduce the issue
- **Affected Versions:** Which versions are affected?
- **Suggested Fix:** If you have a fix in mind, include it

### 4. Response Timeline

We aim to respond to security reports within:

- **Initial Response:** 48 hours
- **Status Update:** 7 days
- **Fix Timeline:** Depends on severity (see below)

## Vulnerability Severity Levels

We follow the [CVSS v3.1](https://www.first.org/cvss/) scoring system:

| Severity | CVSS Score | Response Time |
| -------- | ---------- | ------------- |
| Critical | 9.0-10.0   | 24-48 hours   |
| High     | 7.0-8.9    | 1-7 days      |
| Medium   | 4.0-6.9    | 7-30 days     |
| Low      | 0.1-3.9    | 30-90 days    |

## Security Best Practices for REAPER Users

When using REAPER in your projects:

1. **Keep Dependencies Updated**
   - Regularly update REAPER and its dependencies
   - Enable Dependabot or similar tools
   - Monitor security advisories

2. **Plugin Security**
   - Review plugins before installing (check source code)
   - Only use plugins from trusted sources
   - Follow principle of least privilege for plugin permissions

3. **Data Handling**
   - Never hard-code secrets in plugins
   - Use environment variables for sensitive configuration
   - Implement proper access controls for signal data

4. **Pipeline Isolation**
   - Run untrusted plugins in sandboxed environments
   - Monitor plugin behavior for anomalies
   - Implement rate limiting for external API calls

5. **Input Validation**
   - Validate all external inputs (sources, configurations)
   - Sanitize data before passing to plugins
   - Use Pydantic models for automatic validation

## Security Features in REAPER

REAPER includes several security features:

✅ **Type Safety**
- Pydantic v2 models with strict validation
- Runtime type checking for all data structures

✅ **Plugin Isolation**
- Pluggy-based plugin system with clear boundaries
- No shared state between plugins by default

✅ **Minimal Dependencies**
- Only 2 production dependencies (pluggy, pydantic)
- Reduces attack surface

✅ **CI/CD Security**
- CodeQL security scanning
- Dependency vulnerability checks
- Explicit GitHub Actions permissions

✅ **Code Quality**
- 96% test coverage
- Zero linting violations
- Pre-commit hooks for code review

## Security Disclosure Policy

When a security vulnerability is fixed:

1. **Patch Release:** We release a patch version immediately
2. **Security Advisory:** We publish a GitHub Security Advisory
3. **Public Disclosure:** After users have had time to update (typically 7-14 days)
4. **Credit:** We credit the reporter (unless they prefer to remain anonymous)

## Third-Party Security Tools

We use the following tools to maintain security:

- **CodeQL:** Automated security scanning
- **Dependabot:** Dependency vulnerability alerts
- **Ruff:** Code linting and security checks
- **pytest:** Comprehensive test coverage

## Contact

For non-security-related questions, please:
- Open a [GitHub Issue](https://github.com/SaltProphet/Reaper/issues)
- Start a [Discussion](https://github.com/SaltProphet/Reaper/discussions)
- See [CONTRIBUTING.md](docs/guides/CONTRIBUTING.md) for development questions

For security issues, always use the private reporting channels mentioned above.

---

**Last Updated:** 2026-02-09  
**Policy Version:** 1.0
