# Python Advanced

## Day 1
- r"string" - r tells Python to interpret as raw text (can be used for Windows file paths e.g. r"C:\folder1\folder2")

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
