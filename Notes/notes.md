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
