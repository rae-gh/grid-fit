# Basic integration test for gridfit R binding
library(gridfit)
print(ls("package:gridfit"))

result <- interp_rcpp(0, 1, 1)
stopifnot(identical(result, 0.5))
