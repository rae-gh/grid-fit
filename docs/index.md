# grid-fit Documentation

## Installation

### Python
You can install the Python bindings using pip (after building):

```bash
pip install .
```

### R
You can install the R package using devtools (after building):

```R
# In R
install.packages("devtools")
devtools::install("path/to/grid-fit")
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
