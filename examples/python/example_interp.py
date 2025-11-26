# Example usage of the gridfit Python binding
import gridfit

# Interpolate between 0 and 1 with 1 interval
import time

n = 10000000
start = time.time()
result = gridfit.interp(0, 1, n)
elapsed = time.time() - start
if result is not None and len(result) > 0:
	print(f"n: {len(result)} First: {result[0]}, Last: {result[-1]}")
else:
	print("No points returned.")
print(f"Time taken: {elapsed:.6f} seconds")
