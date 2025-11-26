
# grid-fit

Fast N-dimensional polynomial interpolation on regular grids with Python and R bindings.

## Features
- Trilinear interpolation (faster than scipy)
- Extends naturally to tricubic, higher dimensions
- Python and R bindings
- Efficient precomputed matrix approach

## Installation

### Python
Install directly from GitHub:

```bash
python -m pip install git+https://github.com/rae-gh/grid-fit.git
```

### R
Install directly from GitHub using devtools:

```R
install.packages("devtools")
library(devtools)
install_url("https://github.com/rae-gh/grid-fit/archive/refs/heads/main.zip")
```

## Usage Example

### Python
```python
import gridfit
result = gridfit.interp(0, 1, 1)
print(result)  # [0.5]
```

### R
```R
library(gridfit)
result <- interp(0, 1, 1)
print(result)  # [0.5]
```

---

For development instructions, see the documentation or `DEV.md`.

```

**.gitignore:**
```
# Build artifacts
build/
dist/
*.so
*.dll
*.dylib
*.o

# Python
__pycache__/
*.pyc
*.egg-info/
.pytest_cache/

# R
*.Rcheck/
.Rhistory

# IDE
.vscode/
.idea/
*.swp