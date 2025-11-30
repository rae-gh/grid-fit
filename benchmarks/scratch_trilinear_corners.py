import numpy as np
from scipy.interpolate import RegularGridInterpolator
from gridfit import trilinear  # Your C++ binding

x = y = z = np.arange(2)
points = np.array([[i, j, k] for i in x for j in y for k in z])

for idx in range(8):
    values = np.zeros((2, 2, 2), dtype=np.float32)
    # Set one corner to 1
    i, j, k = (idx >> 2) & 1, (idx >> 1) & 1, idx & 1
    values[i, j, k] = 1.0

    scipy_result = RegularGridInterpolator((x, y, z), values)(points)
    gridfit_result = trilinear(x, y, z, values, points)
    # convert to float and round to 4 decimals for comparison
    scipy_result = np.round(scipy_result.astype(float), 4)
    gridfit_result = np.round(gridfit_result.astype(float), 4)

    print(f"Corner {idx} (set [{i},{j},{k}] = 1):")
    print("  scipy:   ", scipy_result)
    print("  gridfit: ", gridfit_result)
    print()
