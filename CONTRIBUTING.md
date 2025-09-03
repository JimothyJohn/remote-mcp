# Contributing to Remote MCP

Thank you for your interest in contributing to Remote MCP! This guide will help you get started with contributing to this project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Submitting Changes](#submitting-changes)
- [Code of Conduct](#code-of-conduct)

## Getting Started

Remote MCP is a deployment template for hosting remote MCP (Model Context Protocol) servers and generating clients to test against them. The project uses Python 3.11+ and includes both server and client components.

### Prerequisites

- Python 3.11 or higher
- Git
- AWS CLI (for deployment features)
- Basic knowledge of MCP (Model Context Protocol)

## Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/remote-mcp.git
   cd remote-mcp
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e .
   pip install -e .[dev]
   ```

4. **Set Up Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## Making Changes

### Project Structure

```
remote_mcp/
├── remote_mcp/
│   ├── server/           # MCP server implementation
│   │   ├── app.py        # Main application with tools and resources
│   │   ├── tools.py      # Tool implementations
│   │   └── mcp_lambda_handler/  # Lambda handler for AWS deployment
│   └── client/           # Client for testing MCP servers
├── docs/                 # Documentation and GitHub Pages
├── tests/                # Test suite
└── pyproject.toml        # Project configuration
```

### Coding Standards

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable and function names

### Adding New Tools

To add a new MCP tool:

1. **Add the implementation to `tools.py`:**
   ```python
   def your_new_tool(param: str) -> str:
       """Brief description of what the tool does."""
       # Implementation here
       return result
   ```

2. **Register the tool in `app.py`:**
   ```python
   @mcp.tool()
   def your_tool_name(param: str) -> str:
       """Tool description for MCP."""
       return your_new_tool(param)
   ```

### Adding New Resources

To add a new MCP resource:

```python
@mcp.resource("resource://path/{param}")
def get_resource(param: str) -> str:
    """Get resource description."""
    return resource_content
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=remote_mcp

# Run specific test file
pytest tests/test_specific.py

# Run tests in parallel
pytest -n auto
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases
- Mock external dependencies (AWS services, etc.)

Example test structure:
```python
import pytest
from remote_mcp.server.tools import your_function

def test_your_function_success():
    """Test successful execution of your_function."""
    result = your_function("valid_input")
    assert result == "expected_output"

def test_your_function_invalid_input():
    """Test your_function with invalid input."""
    with pytest.raises(ValueError):
        your_function("invalid_input")
```

## Code Quality

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

- **ruff**: Code formatting and linting
- **mypy**: Type checking
- **bandit**: Security analysis
- **safety**: Dependency vulnerability checking

### Manual Quality Checks

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy remote_mcp/

# Security analysis
bandit -r remote_mcp/

# Check dependencies for vulnerabilities
safety check
```

## Submitting Changes

### Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clear, focused commits
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Test Your Changes**
   ```bash
   pytest
   ruff check .
   mypy remote_mcp/
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Use a clear, descriptive title
   - Provide a detailed description of your changes
   - Reference any related issues
   - Include screenshots if UI changes are involved

### Commit Message Guidelines

Use conventional commit format:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions or modifications
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

### Pull Request Review Process

1. Automated checks must pass (tests, linting, type checking)
2. At least one maintainer review is required
3. All conversations must be resolved
4. Branch must be up to date with main

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Assume good intentions

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Unprofessional conduct

## Getting Help

- **Questions**: Open a GitHub issue with the "question" label
- **Bug Reports**: Open a GitHub issue with the "bug" label
- **Feature Requests**: Open a GitHub issue with the "enhancement" label
- **Documentation**: Check the [project documentation](https://jimothyjohn.github.io/remote-mcp/)

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs/learn/server-concepts)
- [FastMCP Framework](https://gofastmcp.com/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)

Thank you for contributing to Remote MCP! 🚀