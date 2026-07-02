# Python Advanced

## Day 1
- `r"<str>"` - `r` tells Python to interpret as raw text (can be used for Windows file paths e.g. `r"C:\folder1\folder2"`)

### Creating .venv
```bash
python -m venv .venv

# Activate environment
.\.venv\Scripts\Activate.ps1

# Deactivate
deactivate
```


### Pre-Commit
- Runs things like linters and tests on your code before you commit
- Will be useful for JAGERS
- Need to run before committing to make sure it passes (if files are changed, need to git add again to stage changes)

#### Installing and Running
```bash
# Install in a .venv
pip install pre-commit

# Create sample config file
pre-commit sample-config > .pre-commit-config.yaml # In Linux


# Activate in Git (in root Git directory)
pre-commit install


## Other commands
# Run over all files manually
pre-commit run --all-files

# Commit without checking
git commit -m "Your message" --no-verify
```

### Pandas
- Chaining encouraged over using intermediate variables/dataframes
- `.pipe()` can be used to insert custom functions into a workflow

```python
# Example: Using .pipe() with a custom function
import pandas as pd

def add_discount(df, percent):
    df['discounted_price'] = df['price'] * (1 - percent / 100)
    return df

def filter_instock(df):
    return df[df['in_stock']]

# Create a sample DataFrame
data = pd.DataFrame({
    'product': ['A', 'B', 'C'],
    'price': [100, 200, 160],
    'in_stock': [True, False, True],
})

# Use .pipe() to insert custom functions into a workflow
# Format for pipe functions with arguments is .pipe(func, arg1, arg2, ...)
result = (
    data
    .pipe(filter_instock)
    .pipe(add_discount, percent=10)
    .sort_values('discounted_price')
)
print(result)
```

- Chaining methods together can make it hard to debug
- Can use a `.pipe()` method to print output at a specific step
```python
# E.g.
def log_step(df: pd.DataFrame, step_name: str | None = None) -> pd.DataFrame:
    """Print a dataframe during a chained method"""
    if step_name:
        print(f"---{step_name}---")

    print(df)
    return df
```

### Bokeh
- Python library like matplotlib that directly creates HTML so you can have interactive plots
- This could be implemented into a python backend and served as a json item to a Next.js frontend (for JO)
- Could be useful for little modules
- Bokeh can also do GIS natively...definitely could be useful


### Decorators
- Wrap a function with standard things it does before/after the function executes
- dataclass is a good example

### Tests

#### Testing FastAPI
**Test Client** - FastAPI provides a testing utility `TestClient` that simulates HTTP requests (like Postman or a frontend browser)

**Fixtures** - In pytest, a fixture is a setup function that runs before your tests. It provides clean, reusable configurations (like creating a mock client or setting up temporary data) so you don't repeat yourself.

**Mocking/Patching** - Don't want to hit real databases in tests, mocking intercepts these system calls and feeds predictable "fake" data instead
- `MagicMock` -> Highly flexible "empty Python object" that automatically creates attributes and methods when you try to access them
    - Will happily accept any method call, with any arguments, and return another mock object (by default)
- `patch` -> Decorator or context manager that temporarily replaces an object at a specific import path with a Mock object

```python
# MagicMock Example
from unittest.mock import MagicMock

# Create a blank stunt double
mock_api = MagicMock()

# Configure what it should return when a specific method is called
mock_api.get_user_status.return_value = {"status": "active"}

# Run it
result = mock_api.get_user_status(user_id=42)

# Check the recording to see if it was called correctly
mock_api.get_user_status.assert_called_once_with(user_id=42)
print(result)  # Output: {"status": "active"}

# ================================================ #

# Patch Example
from unittest.mock import patch
import requests

# Let's say we want to intercept requests.get so it doesn't hit the internet
with patch('requests.get') as mock_get:
    # Inside this block, requests.get is no longer the real function!
    # It has been replaced by a MagicMock automatically.
    mock_get.return_value.status_code = 200

    response = requests.get("https://google.com")
    print(response.status_code)  # Output: 200 (No internet connection actually happened)

# Outside the block, requests.get is completely restored to normal
```


### AI Discussion w/ Mel
- Setting up standard rules for the team
- Probably will have to be in Kiro
- Can maybe orchestrate Kiro as third-party agent within pipeline runners?


Ideas from AI:
- Rules should be short and modular (avoid filling up context window)
- Write in clear imperative language (MUST/MUST NOT)
- Priorities "Anti-Patterns" (DO NOT rules)
    - AI is eager to generate code
    - Can define boundaries for third-party packages etc.
- Steering files should live in Git, and have same modification rules as code
    - Need to go through merge request etc.
- Establish clear boundaries on "vibe mode" vs "spec mode"
    - Vibe mode for minor tasks, general development etc.
    - Spec mode mandatory for any major tasks/changes
- Add a linting step to the CI/CD pipeline that uses the AI to match code against the rules that are defined


Common issues with Kiro and ideas on mitigations:
- Code bloat/over-engineering
    - Enforce minimalist/human-first code style in `structure.md`
    - Demand low complexity
    - Set strict file counts
- Opaque credit burn/hidden costs
    - Ban autonomous loops (human-in-the-loop **only**)
    - Team should use vibe-mode first to flesh out ideas
    - Set credit alerts?
- Circular debugging loops and context failures
    - Outlaw "fix-on-fix" -> If first fix fails, must stop and write a report instead
    - Isolate context
- Slow performance
    - Optimise `.kiroignore`
    - Tries to index entire workspace, not needed
    - Keep context small
- Executing dangerous commands
    - Secure terminal scope
    - Set execution mode to "Acknowledge"
    - Isolate local environments


```markdown
# Examples

structure.md
## AI Code Economy and Simplicity Rules
- CRITICAL: Prioritise code legibility and minimalism. Never create multi-file abstractions when a single file suffices.
- FILE RESTRICTION: A single feature task MUST NOT generate more than 3 new files unless explicitly permitted in the task description.
- NO BOILERPLATE: Do not generate placeholder files, empty utility modules, or excessive inline logging wrappers.
- DRY vs. WET: Prefer slight duplication over complex, deeply nested abstractions that are difficult for humans to audit.


tech.md
## Error Handling and Debugging Guardrails
- CIRCUIT BREAKER: If Kiro introduces a compilation or test failure, it is permitted EXACTLY ONE attempt to fix it.
- If the first fix fails, Kiro MUST STOP generating code, revert its last change, and output a concise summary of the error to the chat panel.
- NO AUXILIARY FILES: Kiro is strictly forbidden from creating new "debug" or "temporary" files to troubleshoot an existing bug.

```
