# Example usage of the gridfit R binding
library(gridfit)

# Interpolate between 0 and 1 with 1 interval
result <- interp(0, 1, 1)
cat("Interpolated points:", result, "\n")
