# Example usage of the gridfit Python trilinear binding
import gridfit
import numpy as np

x = np.array([0.0, 1.0], dtype=np.float32)
y = np.array([0.0, 1.0], dtype=np.float32)
z = np.array([0.0, 1.0], dtype=np.float32)
values = np.array([0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0], dtype=np.float32)
points = np.array([[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]], dtype=np.float32)
tri_result = gridfit.trilinear(x, y, z, values, points)
print("trilinear dummy output:", tri_result)
