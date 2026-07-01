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
