# Example usage of the gridfit R binding
library(gridfit)

# Interpolate between 0 and 1 with 1 interval
result1 <- interp_rcpp(0, 1, 1)
cat("Interpolated points (n=1):", result1, "\n")

# Interpolate between 0 and 1 with 1000 intervals and time it
n <- 10000000
start_time <- Sys.time()
result2 <- interp_rcpp(0, 1, n)
end_time <- Sys.time()
elapsed <- end_time - start_time
cat(sprintf(
	"n = %d, first = %g, last = %g\n",
	n, result2[1], result2[length(result2)]
))
cat(sprintf("Time taken: %.6f seconds\n", as.numeric(elapsed, units="secs")))
