# Contributing to Bluefin

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bluefin.git
cd bluefin
```

2. Create and activate conda environment:
```bash
conda create -n bluefin python=3.12
conda activate bluefin
```

3. Install dependencies:
```bash
pip install polars requests
```

## Code Style

- Use functional programming approach
- Type hints are required for all functions
- Maximum line length: 100 characters
- Use docstrings for all functions and classes

## Git Workflow

### Commit Messages

Use semantic commit messages:
- `feat:` New features
- `fix:` Bug fixes
- `chore:` Maintenance tasks
- `docs:` Documentation updates
- `style:` Code style changes
- `refactor:` Code restructuring
- `test:` Adding tests

Example:
```
feat: add line movement tracking to prop updates
```

### Branches

- `main`: Production-ready code
- `develop`: Development branch
- Feature branches: `feature/description`
- Bug fixes: `fix/description`

## Data Management

### Directory Structure

- Keep data files in appropriate YYYY-MM directories
- Use consistent file naming: `YYYY-MM-DD_[source].json`
- Don't commit data files (they're in .gitignore)

### Data Updates

When updating props:
1. Check existing data first
2. Track all changes in metadata
3. Use appropriate delay between API calls

## Error Handling

- Always use try/except blocks for external calls
- Log errors appropriately
- Use retry mechanism for API calls
- Handle rate limits gracefully

## Testing

(To be implemented)
- Unit tests for core functions
- Integration tests for API calls
- Test data validation 