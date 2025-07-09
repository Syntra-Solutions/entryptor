# Entryptor CI/CD Pipelines

This directory contains Azure DevOps pipeline configurations for building, testing, and deploying Entryptor.

## Pipeline Files

### `azure-pipelines.yml` - Comprehensive CI/CD Pipeline
**Multi-stage pipeline with templates**
- ✅ Multi-platform testing (Linux, macOS, Windows)
- ✅ Multiple Python versions (3.8-3.12)
- ✅ Code quality checks (Ruff, MyPy)
- ✅ Test coverage reporting
- ✅ Cross-platform builds with PyInstaller
- ✅ Release packaging and artifacts
- ✅ Modular template structure

**Triggers:**
- `main` branch
- Pull requests

## Templates (Pipeline Structure)

### `templates/test-steps.yml`
Reusable testing steps including:
- Dependency installation
- Code linting with Ruff
- Type checking with MyPy
- Test execution with pytest
- Coverage reporting
- Import validation

### `templates/build-steps.yml`
Platform-specific build steps:
- PyInstaller configuration for each OS
- Binary artifact creation
- Build verification
- Distribution preparation

### `templates/package-steps.yml`
Release packaging:
- Multi-platform artifact collection
- Archive creation (tar.gz, zip)
- Source distribution
- Checksum generation
- Release notes creation

## Setup Instructions

### Option 1: Quick Setup (Recommended)
1. Copy `azure-pipelines.yml` to your repository root
2. Configure Azure DevOps to use this pipeline

### Option 2: Advanced Setup
1. Copy the entire `Pipelines` folder to your repository
2. Use `Pipelines/azure-pipelines.yml` as your main pipeline
3. Configure Azure DevOps pipeline path: `Pipelines/azure-pipelines.yml`

## Pipeline Stages

### 🧪 Test Stage
- **Multi-Python Testing**: Tests on Python 3.8-3.12 (Linux)
- **Cross-Platform Testing**: Core functionality on Linux, macOS, Windows
- **Code Quality**: Linting, type checking, coverage analysis

### 🔨 Build Stage
- **Linux Build**: Creates standalone Linux executable
- **macOS Build**: Creates macOS application bundle
- **Windows Build**: Creates Windows executable
- **Artifacts**: Published for download/deployment

### 📦 Package Stage (Advanced only)
- **Release Creation**: Only runs on `1.0.0` branch
- **Multi-Platform Archives**: Creates distribution packages
- **Source Distribution**: Python package (wheel/sdist)
- **Release Notes**: Auto-generated documentation

## Requirements

### Repository Structure
```
├── src/                 # Source code
├── tests/              # Test files
├── requirements.txt    # Runtime dependencies
├── requirements-dev.txt # Development dependencies
├── pyproject.toml      # Project configuration
└── Pipelines/          # CI/CD configurations
```

### Dependencies
The pipeline expects these files in your repository:
- `requirements.txt` - Runtime dependencies
- `requirements-dev.txt` - Development dependencies (ruff, mypy, pytest, etc.)
- `src/main.py` - Application entry point

## Azure DevOps Configuration

### 1. Create Pipeline
1. Go to Azure DevOps → Pipelines → New Pipeline
2. Choose "Azure Repos Git"
3. Select your repository
4. Choose "Existing Azure Pipelines YAML file"
5. Select the pipeline file path

### 2. Configure Variables (Optional)
- `pythonVersion`: Default Python version (default: '3.11')
- Custom build configurations can be added

### 3. Branch Policies
Consider setting up branch policies for:
- `main` branch: Require pipeline success
- `1.0.0` branch: Require pipeline success + approvals

## Artifacts

### Test Artifacts
- Test results (JUnit XML)
- Code coverage reports (Cobertura XML + HTML)

### Build Artifacts
- `entryptor-linux`: Linux executable + docs
- `entryptor-macos`: macOS executable + docs  
- `entryptor-windows`: Windows executable + docs

### Release Artifacts (Advanced)
- `entryptor-release`: Complete release package
  - Platform-specific archives
  - Source distribution
  - Checksums
  - Release notes

## Troubleshooting

### Common Issues
1. **Missing main.py**: Ensure `src/main.py` exists as entry point
2. **Import Errors**: Check PyInstaller hidden imports
3. **Platform Issues**: Verify cross-platform dependencies
4. **Permission Issues**: Ensure executable permissions on built binaries

### Debugging
- Check pipeline logs for specific error messages
- Test builds locally with PyInstaller
- Verify all requirements files are complete

## Customization

### Adding New Platforms
Modify the strategy matrix in build jobs:
```yaml
strategy:
  matrix:
    YourPlatform:
      imageName: 'your-vm-image'
      artifactName: 'entryptor-yourplatform'
```

### Custom Build Options
Modify PyInstaller commands in build steps:
- Add icons: `--icon=path/to/icon`
- Add resources: `--add-data "src:dest"`
- Hide console: `--windowed`
- Single file: `--onefile`

### Additional Quality Gates
Add steps to test templates:
- Security scanning
- Performance tests
- Integration tests
- Documentation generation
