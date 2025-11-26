# Basic integration test for gridfit R binding
library(gridfit)

result <- interp(0, 1, 1)
stopifnot(identical(result, 0.5))
