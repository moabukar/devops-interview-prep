# Contributing to DevOps Interview Prep

Thank you for your interest in contributing! This project helps thousands of professionals prepare for DevOps interviews.

## Quick Start

```bash
git clone https://github.com/moabukar/mockops.git
cd mockops
make setup  # Install dependencies and pre-commit hooks
make test   # Verify everything works
```

## Ways to Contribute

### 1. Adding Questions
The most valuable contribution is high-quality interview questions based on real experiences.

**Requirements:**
- Based on actual interview questions
- Include realistic scenarios
- Provide detailed explanations
- Test practical knowledge, not memorization

**Process:**
```bash
make add-question  # Interactive question builder
make validate-questions  # Validate format
```

### 2. Code Improvements
- Bug fixes
- Performance improvements  
- New CLI features
- Better user experience

### 3. Documentation
- Improve README
- Add examples
- Create tutorials
- Fix typos

## Development Workflow

### Setup
```bash
make setup          # Full development setup
make install-dev    # Install in development mode
make install-pre-commit  # Install git hooks
```

### Code Quality
```bash
make format         # Format code (black, isort)
make lint          # Run linters (flake8, mypy)
make test          # Run test suite
make check         # Run all quality checks
```

### Testing
```bash
make test          # Run all tests
make test-fast     # Skip slow tests
make test-cov      # Generate coverage report
```

## Question Guidelines

### Question Structure
```json
{
  "id": "topic-###",
  "topic": "aws|kubernetes|docker|linux|git|networking|terraform|cicd|security|monitoring|ansible|azure",
  "difficulty": "easy|medium|hard",
  "question": "Clear, specific question",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct_answer": 2,
  "explanation": "Detailed explanation with reasoning",
  "scenario": "Real-world context (optional)",
  "company_tags": ["faang", "startup", "enterprise"],
  "real_world_context": "How this applies in practice (optional)"
}
```

### Quality Standards

**Good Questions:**
- Test understanding, not memorization
- Include realistic scenarios
- Have clear, unambiguous answers
- Provide educational explanations

**Avoid:**
- Trick questions or gotchas
- Overly specific syntax questions
- Questions with subjective answers
- Outdated technologies

### Difficulty Levels
- **Easy**: Fundamental concepts, basic commands
- **Medium**: Practical scenarios, troubleshooting
- **Hard**: Architecture decisions, complex debugging

## Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **mypy** for type checking

Run `make format lint` before committing.

## Testing

### Writing Tests
```python
# tests/test_new_feature.py
import pytest
from devops_ip.cli import InterviewSession

def test_session_scoring():
    session = InterviewSession(track_progress=False)
    assert session.score == 0
    assert session.total == 0
```

### Test Categories
- **Unit tests**: Test individual functions
- **Integration tests**: Test CLI commands
- **Slow tests**: Mark with `@pytest.mark.slow`

## Pull Request Process

1. **Fork and branch**
   ```bash
   git checkout -b feature/new-aws-questions
   ```

2. **Make changes**
   - Add questions or code
   - Write/update tests
   - Update documentation

3. **Quality checks**
   ```bash
   make check  # Run all quality checks
   make validate-questions  # Validate questions
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "Add 10 new AWS security questions
   
   - Focus on IAM and S3 security scenarios
   - Include real-world context from recent interviews
   - Add company tags for FAANG and enterprise"
   ```

5. **Create Pull Request**
   - Use the provided template
   - Reference any related issues
   - Include testing instructions

## Pull Request Template

```markdown
## What this PR does
Brief description of changes

## Type of Change
- [ ] New questions
- [ ] Bug fix  
- [ ] New feature
- [ ] Documentation

## Questions Added (if applicable)
- Topic: aws
- Count: 5 questions
- Difficulty: 2 easy, 2 medium, 1 hard
- Source: Recent FAANG interviews

## Testing
- [ ] Tests pass (`make test`)
- [ ] Questions validated (`make validate-questions`)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated (for significant changes)
```

## Issue Templates

### Bug Report
Use for:
- CLI crashes or errors
- Incorrect question answers
- Performance issues

### Feature Request  
Use for:
- New CLI commands
- Enhanced functionality
- User experience improvements

### Question Submission
Use for:
- Submitting individual questions
- Requesting new topic areas
- Reporting question quality issues

## Recognition

Contributors are recognized in:
- README.md
- Release notes
- GitHub contributors page

Significant contributions may receive:
- Maintainer status
- Special recognition in project documentation

## Code of Conduct

- Be respectful and inclusive
- Focus on helping interview candidates succeed
- Provide constructive feedback
- Share knowledge generously

## Getting Help

- **Questions**: Open a GitHub discussion
- **Issues**: File a GitHub issue
- **Chat**: Tag @moabukar in issues/PRs

## Development Tips

### Adding New CLI Commands
```python
@cli.command()
@click.option('--example', help='Example option')
def new_command(example):
    """New command description"""
    click.echo("Hello from new command!")
```

### Question Validation
```bash
# Validate single question
python scripts/validate_questions.py --id aws-001

# Validate all questions
make validate-questions
```

### Local Testing
```bash
# Test CLI locally
devops-ip practice aws --count 1

# Test Docker build
make docker-build docker-test
```

---

**Thank you for contributing to DevOps Interview Prep!**