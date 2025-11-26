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
