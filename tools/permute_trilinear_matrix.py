import numpy as np

# Paste your original 8x8 matrix here (row-major, as in C++)
mat = np.array(
    [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [-1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, -1.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [-1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        [1.0, -1.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0],
        [1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 1.0, 0.0],
        [-1.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0],
    ]
)
old_order = [0, 1, 2, 3, 4, 5, 6, 7]

new_orders = []
new_orders.append([0, 4, 2, 6, 1, 5, 3, 7])  # (x, y, z) -> (z, y, x)


for new_order in new_orders:
    # Compute the permutation indices
    perm = [old_order.index(i) for i in new_order]

    # Permute both rows and columns
    mat_permuted = mat[np.ix_(perm, perm)]

    # Print as C++ initializer
    print("Permuted matrix (C++ initializer):")
    for row in mat_permuted:
        print("    " + ", ".join(f"{v:.16g}" for v in row) + ",")
    mat = mat_permuted
