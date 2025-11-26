// Example usage of the gridfit C++ trilinear function
#include <iostream>
#include <vector>
#include "../../include/interp.h"

int main() {
    std::vector<float> x = {0.0f, 1.0f};
    std::vector<float> y = {0.0f, 1.0f};
    std::vector<float> z = {0.0f, 1.0f};
    std::vector<float> values = {0.0f, 1.0f, 1.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f};
    // Points as 2x3 matrix, flatten to 1D vector (row-major)
    std::vector<std::vector<float>> points2d = {{0.5f, 0.5f, 0.5f}, {0.1f, 0.2f, 0.3f}};
    std::vector<float> points_flat;
    for (const auto& row : points2d) {
        points_flat.insert(points_flat.end(), row.begin(), row.end());
    }
    int n_points = points2d.size();
    int n_dim = points2d[0].size();
    auto tri_result = trilinear(x, y, z, values, points_flat, n_points, n_dim);
    std::cout << "trilinear dummy output: ";
    for (auto v : tri_result) std::cout << v << " ";
    std::cout << std::endl;
    return 0;
}
