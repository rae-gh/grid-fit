# Test for gridfit trilinear_rcpp dummy output
library(gridfit)

x <- c(0, 1)
y <- c(0, 1)
z <- c(0, 1)
values <- c(0, 1, 1, 0, 1, 0, 0, 1)
points <- matrix(c(0.5, 0.5, 0.5,
                   0.1, 0.2, 0.3), ncol=3, byrow=TRUE)
result <- trilinear_rcpp(x, y, z, values, points)
stopifnot(all(result == 42.0))
