# grid-fit Documentation


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
# Interpolate between 0 and 1 with 1 interval
result = gridfit.interp(0, 1, 1)
print(result)  # [0.5]
```

### R
```R
library(gridfit)
# Interpolate between 0 and 1 with 1 interval
result <- interp(0, 1, 1)
print(result)  # [0.5]
```

---

For more details, see the README or source code.
