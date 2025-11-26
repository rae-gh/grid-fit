#include "interp.h"
#include <vector>


std::vector<float> interp(double a, double b, int n) {
    std::vector<float> result;
    if (n <= 0) return result;
    result.reserve(n);
    float fa = static_cast<float>(a);
    float fb = static_cast<float>(b);
    float step = (fb - fa) / (n + 1);
    for (int i = 1; i <= n; ++i) {
        result.push_back(fa + step * i);
    }
    return result;
}

// Dummy trilinear interpolation: returns a vector of 42.0f for each point
std::vector<float> trilinear(
    const std::vector<float>& x,
    const std::vector<float>& y,
    const std::vector<float>& z,
    const std::vector<float>& values,
    const std::vector<float>& points,
    int n_points,
    int ndim
) {
    std::vector<float> result;
    result.resize(n_points, 42.0f); // Dummy value
    return result;
}
