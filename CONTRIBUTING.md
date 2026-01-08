# Contributing to Sigandwa

## Overview

Sigandwa is a serious analytical platform treating Biblical and historical data as an authoritative dataset for pattern recognition and civilizational analysis.

Contributions are welcome, but must maintain the system's analytical rigor and avoid speculation.

---

## Core Principles

Before contributing, understand these non-negotiable principles:

1. **Historical Accuracy Over Interpretation**
   - Data must be verifiable
   - Sources must be cited
   - Uncertainty must be explicit

2. **Pattern Recognition, Not Prediction**
   - The system identifies historical analogs
   - It does NOT set dates for future events
   - All projections are conditional trajectories

3. **No Ideological Agenda**
   - This is not theology
   - This is not political advocacy
   - This is analytical modeling

4. **Code Quality Matters**
   - Clean, documented code
   - Type hints required
   - Tests for new features

---

## How to Contribute

### Reporting Issues

Use GitHub Issues for:
- Bug reports
- Data inaccuracies
- Performance problems
- Documentation gaps

**Template**:
```markdown
**Issue Type**: [Bug / Data / Performance / Docs]
**Component**: [Chronology / API / Database / Frontend]
**Description**: Clear description of the issue
**Steps to Reproduce**: 
1. Step one
2. Step two
**Expected Behavior**: What should happen
**Actual Behavior**: What actually happens
**Environment**: OS, Python version, Docker version
```

---

### Adding Historical Data

#### Biblical Events

1. Edit `data/seed/biblical_timeline.py`
2. Follow existing format:
```python
{
    "name": "Event Name",
    "description": "Clear description",
    "year_start": -1000,  # Ussher-based
    "year_end": -990,  # Optional
    "year_start_min": -1010,  # If uncertain
    "year_start_max": -990,   # If uncertain
    "era": "UNITED_MONARCHY",
    "event_type": "POLITICAL",
    "biblical_source": "1 Kings 10:1-13",
    "metadata": {
        "pattern": "relevant_pattern_name",
        "significance": "Why this matters"
    }
}
```

3. **Required**:
   - Biblical source citation
   - Year based on Ussher chronology (or note uncertainty)
   - Clear description
   - Appropriate era and type

4. Submit PR with justification

#### Historical Continuation

1. Edit `data/seed/historical_continuation.py`
2. Same format as above, but:
   - Use `historical_source` instead of `biblical_source`
   - Cite reputable historical sources
   - For modern events, cite multiple sources

---

### Code Contributions

#### Setting Up Development Environment

```bash
# Fork repository
git clone git@github.com:YOUR_USERNAME/sigandwa.git
cd sigandwa

# Run setup
./setup.sh

# Create feature branch
git checkout -b feature/your-feature-name
```

#### Code Standards

**Python**:
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Format with Black: `black app/`
- Lint with Ruff: `ruff check app/`

**Example**:
```python
def calculate_temporal_distance(
    self, event1_id: int, event2_id: int
) -> Optional[int]:
    """
    Calculate years between two events.

    Args:
        event1_id: ID of first event
        event2_id: ID of second event

    Returns:
        Number of years between events (negative if event1 is later)
        None if either event doesn't exist
    """
    # Implementation
```

#### Testing Requirements

All new features MUST include tests:

```python
# backend/tests/test_your_feature.py
import pytest
from app.your_module import YourClass

def test_your_functionality():
    """Test that your feature works correctly."""
    result = your_function(input_data)
    assert result == expected_output
```

Run tests:
```bash
cd backend
pytest
```

#### Commit Messages

Follow conventional commits:

```
type(scope): brief description

Longer explanation if needed.

- Bullet points for details
- Reference issues: #123
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```
feat(chronology): add support for uncertainty ranges

Implements year_start_min and year_start_max fields
to handle events with imprecise dating.

- Updates ChronologyEngine.add_event()
- Adds validation in Pydantic schemas
- Includes tests for uncertain dates
```

---

### Pull Request Process

1. **Create PR** with clear description
2. **Link Issues**: Reference related issues
3. **Update Documentation**: If adding features
4. **Pass CI Checks**: All tests must pass
5. **Code Review**: Address reviewer feedback
6. **Squash Commits**: Before merge

**PR Template**:
```markdown
## Description
Clear description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Data addition
- [ ] Documentation
- [ ] Refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests pass locally
- [ ] Manually tested

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear
```

---

## Areas for Contribution

### High Priority

1. **Pattern Library** — Implement pattern recognition module
2. **Simulation Engine** — Build trajectory modeling
3. **Prophecy Mapper** — Link prophecies to fulfillments
4. **Frontend** — Next.js dashboard with D3.js visualizations
5. **Data Expansion** — More historical events with citations

### Medium Priority

1. **API Authentication** — JWT-based security
2. **Rate Limiting** — Protect API from abuse
3. **Export Functionality** — PDF reports, CSV datasets
4. **Caching Layer** — Redis integration
5. **Performance Optimization** — Query tuning

### Low Priority

1. **Mobile App** — React Native client
2. **CLI Tool** — Command-line interface
3. **Data Import** — Bulk import from CSV/JSON
4. **Visualization Library** — Reusable chart components

---

## Documentation Contributions

Documentation improvements are always welcome:

- API examples
- Architecture clarifications
- Tutorial walkthroughs
- Deployment guides
- Troubleshooting tips

---

## Data Quality Guidelines

### Biblical Events

**Acceptable**:
- Events with clear Biblical references
- Ussher chronology or scholarly alternatives (with notes)
- Uncertainty ranges when dates are disputed

**Not Acceptable**:
- Events without Biblical support
- Purely interpretive additions
- Date-setting for prophetic fulfillments

### Historical Events

**Acceptable**:
- Well-documented historical events
- Multiple source citations
- Clear connection to Biblical patterns

**Not Acceptable**:
- Speculative connections
- Conspiracy theories
- Modern political advocacy disguised as history

---

## Community Guidelines

### Be Respectful

- Assume good intentions
- Critique ideas, not people
- Focus on data and logic

### Be Scholarly

- Cite sources
- Admit uncertainty
- Separate fact from interpretation

### Be Constructive

- Offer solutions, not just criticism
- Help newcomers
- Improve documentation

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

- Open a GitHub Discussion
- Review existing documentation
- Check closed issues for similar questions

---

## Recognition

Contributors will be acknowledged in:
- README.md Contributors section
- Release notes
- Project documentation

Significant contributions may earn:
- Maintainer status
- Decision-making input
- Public recognition

---

Thank you for contributing to Sigandwa!
