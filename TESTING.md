# Testing Guide for OpenRemote MCP Server

This document explains how to run and manage tests for the OpenRemote MCP Server.

## Table of Contents
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Structure](#test-structure)
- [Writing Tests](#writing-tests)
- [Coverage Reports](#coverage-reports)
- [Troubleshooting](#troubleshooting)

## Installation

### 1. Install Test Dependencies

First, sync all dependencies including test dependencies:

```powershell
uv sync --extra test
```

This will install:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking utilities
- `httpx` - HTTP client for testing

### 2. Verify Installation

Check that pytest is installed:

```powershell
uv run pytest --version
```

## Running Tests

### Run All Tests

```powershell
uv run pytest
```

### Run Tests with Verbose Output

```powershell
uv run pytest -v
```

### Run Tests with Coverage

```powershell
uv run pytest --cov=app --cov=services --cov-report=html --cov-report=term-missing
```

This generates:
- HTML coverage report in `htmlcov/index.html`
- Terminal output showing coverage percentages

### Run Specific Test Files

```powershell
# Test only MCP server tests
uv run pytest tests/mcp-server/

# Test a specific file
uv run pytest tests/mcp-server/test_services_asset.py

# Test a specific class
uv run pytest tests/mcp-server/test_services_asset.py::TestAssetService

# Test a specific test function
uv run pytest tests/mcp-server/test_services_asset.py::TestAssetService::test_asset_query_success

# Run infrastructure tests
uv run pytest tests/test_infrastructure.py

# Run integration tests
uv run pytest tests/test_integration.py
```

### Run Tests by Marker

```powershell
# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration

# Run all tests except slow ones
uv run pytest -m "not slow"

# Run unit tests with coverage
uv run pytest -m unit --cov=app --cov=services
```

### Run Tests in Parallel (faster)

```powershell
# Install pytest-xdist first
uv pip install pytest-xdist

# Run tests in parallel
uv run pytest -n auto
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures and configuration
├── test_integration.py            # End-to-end integration tests
├── test_infrastructure.py         # Infrastructure tests
└── mcp-server/                    # Tests for MCP server
    ├── __init__.py
    ├── test_server_config.py      # Configuration tests
    ├── test_server_health.py      # Health endpoint tests
    ├── test_services_asset.py     # Asset service tests
    ├── test_services_realm.py     # Realm service tests
    ├── test_services_asset_model.py  # Asset model service tests
    └── test_services_rule.py      # Rule service tests
```

**Note**: After the monolith split, only MCP server tests remain in this repository.

### Test Markers

- `@pytest.mark.unit` - Fast, isolated unit tests
- `@pytest.mark.integration` - Tests that test multiple components together
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.asyncio` - Async tests (automatically applied)

## Writing Tests

### Example Unit Test

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

class TestMyFeature:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_my_function(self, mock_openremote_client):
        """Test description."""
        # Arrange
        mock_openremote_client.some_method = AsyncMock(return_value="result")
        
        # Act
        result = await my_function()
        
        # Assert
        assert result == "expected"
        mock_openremote_client.some_method.assert_called_once()
```

### Using Fixtures

Common fixtures are defined in `tests/conftest.py`:

- `mock_openremote_client` - Mocked OpenRemote client
- `mock_env_vars` - Set up environment variables (automatically configured)
- `sample_asset` - Sample asset data
- `sample_ruleset` - Sample ruleset data

**Note**: Environment variables are automatically set in `conftest.py` to prevent validation errors during imports.

### Testing Async Functions

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### Mocking Dependencies

```python
@pytest.mark.unit
@pytest.mark.asyncio
async def test_with_mock(mock_openremote_client):
    with patch('app.services.asset.get_openremote_service') as mock_get_service:
        mock_service = MagicMock()
        mock_service.client = mock_openremote_client
        mock_get_service.return_value = mock_service
        
        from app.services.asset import query
        
        # Call the function
        result = await query.fn(query_params)
        
        # Your assertions here
```

## Coverage Reports

### Generate HTML Coverage Report

```powershell
uv run pytest --cov=app --cov=services --cov-report=html
```

Open `htmlcov/index.html` in your browser to see detailed coverage.

### View Coverage in Terminal

```powershell
uv run pytest --cov=app --cov=services --cov-report=term-missing
```

This shows which lines are not covered by tests.

### Coverage Configuration

Coverage is configured in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["app", "services"]

[tool.pytest.ini_options]
addopts = ["-v", "--strict-markers", "--tb=short"]
```

### Coverage Goals

Aim for:
- **Unit tests**: 80%+ coverage
- **Integration tests**: Cover critical paths
- **Overall**: 70%+ coverage

**Current Status**: The MCP server tests achieve ~78% coverage (32 tests passing).

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Install dependencies
        run: uv sync --extra test
      
      - name: Run tests
        run: uv run pytest --cov=app --cov=services --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## Troubleshooting

### Import Errors

If you see `Import "pytest" could not be resolved`:

1. Install test dependencies:
   ```powershell
   uv sync --extra test
   ```

2. Configure Python interpreter in VS Code:
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose the uv-managed Python environment

3. Restart VS Code

### Tests Fail to Run

1. Make sure you're in the project root directory
2. Verify environment variables are set (or use fixtures)
3. Check that all dependencies are installed: `uv sync --extra test`

### Slow Tests

1. Use test markers to skip slow tests during development:
   ```powershell
   uv run pytest -m "not slow"
   ```

2. Run tests in parallel:
   ```powershell
   uv pip install pytest-xdist
   uv run pytest -n auto
   ```

### Mock Issues

If mocks aren't working:
- Ensure you're patching at the right location (where it's used, not defined)
- Use `AsyncMock` for async functions
- Check that return values match expected types

## Best Practices

1. **Write tests first** (TDD) when adding new features
2. **Keep tests fast** - use mocks for external dependencies
3. **Test edge cases** - not just happy paths
4. **Use descriptive test names** - they serve as documentation
5. **One assertion per test** (when possible)
6. **Arrange-Act-Assert** pattern for clarity
7. **Don't test implementation details** - test behavior
8. **Keep tests isolated** - no dependencies between tests

## Quick Reference

```powershell
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov=services

# Run specific markers
uv run pytest -m unit
uv run pytest -m integration

# Run specific file
uv run pytest tests/mcp-server/test_services_asset.py

# Run with verbose output
uv run pytest -v

# Run and stop on first failure
uv run pytest -x

# Run and show local variables on failure
uv run pytest -l

# Run last failed tests only
uv run pytest --lf

# Show print statements
uv run pytest -s
```

## Support

For questions or issues:
1. Check this documentation
2. Review test examples in `tests/` directory
3. Check pytest documentation: https://docs.pytest.org/
4. Review project README.md
