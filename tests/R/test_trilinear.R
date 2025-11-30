# Test for gridfit trilinear_rcpp dummy output
library(gridfit)

x <- c(0, 1)
y <- c(0, 1)
z <- c(0, 1)
values <- c(1, 2, 3, 4, 5, 6, 7, 8)
points <- matrix(c(0.5, 0.5, 0.5), ncol=3, byrow=TRUE)
result <- trilinear_rcpp(x, y, z, values, points)
stopifnot(all(result == 4.5))
