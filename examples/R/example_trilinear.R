# Example usage of the gridfit R trilinear binding
library(gridfit)

x <- c(0, 1)
y <- c(0, 1)
z <- c(0, 1)
values <- c(0, 1, 1, 0, 1, 0, 0, 1)
points <- matrix(c(0.5, 0.5, 0.5,
                   0.1, 0.2, 0.3), ncol=3, byrow=TRUE)
tri_result <- trilinear_rcpp(x, y, z, values, points)
cat("trilinear dummy output:", tri_result, "\n")
