# GitHub Actions CI/CD Pipeline Documentation

## Overview

This repository includes a comprehensive GitHub Actions workflow that mirrors our Azure DevOps pipeline structure, providing full CI/CD capabilities for the Entryptor application.

## Workflow Files

### `ci-cd.yml` - Comprehensive CI/CD Pipeline
**Triggers**: Push to `main` or `STAGING`, PRs to `main`

**Features**:
- **Multi-Python Version Testing**: Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Cross-Platform Testing**: Linux, macOS, Windows
- **Build Artifacts**: Creates distributable packages for all platforms
- **Release Packaging**: Combines all artifacts when merging to main
- **Comprehensive Testing**: Unit tests, integration tests, code quality

**Stages**:
1. **Test Multiple Python Versions** (Ubuntu + all Python versions)
2. **Test Cross-Platform** (All OS + Python 3.11)
3. **Build Artifacts** (All platforms, depends on tests)
4. **Create Release** (Ubuntu, main branch only)
- **Code Quality**: ruff, mypy validation
## Pipeline Comparison

| Feature | Azure DevOps | GitHub Actions |
|---------|---------------|----------------|
| Multi-Python Testing | ✅ | ✅ |
| Cross-Platform Testing | ✅ | ✅ |
| Build Artifacts | ✅ | ✅ |
| Code Quality Checks | ✅ | ✅ |
| GUI Testing Support | ✅ | ✅ |
| Execution Time | ~15-20 min | ~15-20 min |

## Workflow Usage

### CI/CD Pipeline (`ci-cd.yml`)
**Ideal for:**
- **Production releases** to main branch
- **Feature development** on STAGING branch
- **Pull request validation**
- **Comprehensive validation** before merges
- **Multi-platform compatibility** verification
- **Release candidate** preparation

## Branch Strategy Integration

Our GitHub Actions workflow integrates with the branch strategy:

```
main (production)
  ├── Full CI/CD pipeline
  ├── All platforms + Python versions
  └── Release artifact creation

STAGING (development)
  ├── Full CI/CD pipeline
  ├── All platforms + Python versions
  └── Comprehensive validation
```

## Artifact Management

### Build Artifacts
- **Linux**: `entryptor-linux.tar.gz`
- **macOS**: `entryptor-macos.tar.gz`  
- **Windows**: `entryptor-windows.zip`
- **Retention**: 30 days for individual builds, 90 days for releases

### Download Artifacts
1. Go to repository **Actions** tab
2. Select successful workflow run
3. Scroll to **Artifacts** section
4. Download platform-specific builds

## Environment Variables

### Global Settings
```yaml
PYTHON_VERSION: '3.11'  # Primary Python version
```

### Platform-Specific Dependencies
- **Linux**: Qt6 base development packages, Xvfb for headless GUI testing
- **macOS**: Native Qt6 support through PyQt6
- **Windows**: Native Qt6 support through PyQt6

## Caching Strategy

All workflows use intelligent caching:
- **pip cache**: Platform and Python version specific
- **Cache keys**: Include requirements file hashes for invalidation
- **Fallback keys**: Graceful degradation for cache misses

## Testing Configuration

### GUI Testing
- **Linux**: Uses Xvfb for headless display
- **macOS/Windows**: Native display support
- **PyQt6**: Full compatibility across all platforms

### Test Execution
```bash
# Core tests (crypto, utils)
pytest tests/test_crypto/ tests/test_utils/ -v

# Integration tests
pytest tests/test_integration.py -v

# All tests with GUI support
xvfb-run -a pytest tests/ -v  # Linux
pytest tests/ -v              # macOS/Windows
```

## Build Process

### PyInstaller Configuration
```bash
python -m PyInstaller \
  --clean \
  --noconfirm \
  --name "Entryptor" \
  --windowed \
  --onedir \
  --add-data "src:src" \
  src/main.py
```

### Output Structure
```
dist/
└── Entryptor/
    ├── Entryptor          # Executable
    ├── _internal/         # Dependencies
    └── src/              # Source files
```

## Monitoring and Notifications

### Status Badges
Add to README.md:
```markdown
[![CI/CD Pipeline](https://github.com/Syntra-Solutions/entryptor/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Syntra-Solutions/entryptor/actions/workflows/ci-cd.yml)
```

### Failure Notifications
- **Email**: Automatic on workflow failure
- **GitHub UI**: Red/green status indicators
- **PR Checks**: Automatic PR status updates

## Troubleshooting

### Common Issues

#### PyQt6 Import Errors
```yaml
# Solution: Install Qt6 development packages
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y qt6-base-dev
```

#### GUI Test Failures on Linux
```yaml
# Solution: Use headless display
- name: Run tests with virtual display
  run: xvfb-run -a pytest tests/ -v
```

#### Cache Issues
```yaml
# Solution: Use cache versioning
key: ${{ runner.os }}-pip-v2-${{ hashFiles('**/requirements*.txt') }}
```

### Debug Steps
1. Check workflow logs in Actions tab
2. Verify requirements.txt changes
3. Test locally with same Python version
4. Check platform-specific dependencies

## Security Considerations

### Secrets Management
- No secrets required for current workflows
- Future: Add secrets for deployment keys if needed

### Permissions
- **Contents**: Read (checkout code)
- **Actions**: Read (download artifacts)
- **Pull Requests**: Write (status updates)

## Future Enhancements

### Planned Improvements
- [ ] **Code coverage reporting** with codecov
- [ ] **Security scanning** with CodeQL
- [ ] **Dependency vulnerability** scanning
- [ ] **Performance benchmarking**
- [ ] **Automated releases** with semantic versioning

### Integration Opportunities
- [ ] **Slack notifications** for team updates
- [ ] **Jira integration** for task tracking
- [ ] **Docker containerization** for consistent builds
- [ ] **Cloud deployment** for demo environments

## Maintenance

### Regular Tasks
- **Monthly**: Review and update action versions
- **Quarterly**: Update Python version matrix
- **As needed**: Adjust caching strategies
- **Per release**: Update artifact retention policies

### Action Updates
```yaml
# Keep actions up to date
- uses: actions/checkout@v4          # Latest stable
- uses: actions/setup-python@v4      # Latest stable  
- uses: actions/cache@v3             # Latest stable
- uses: actions/upload-artifact@v3   # Latest stable
```

---

**Last Updated**: July 8, 2025  
**Maintained By**: Development Team  
**Review Schedule**: Monthly
