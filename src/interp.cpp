#include "interp.h"
#include <vector>

std::vector<float> interp(double a, double b, int n) {
    std::vector<float> result;
    if (n <= 0) return result;
    float step = (b - a) / (n + 1);
    for (int i = 1; i <= n; ++i) {
        result.push_back(a + step * i);
    }
    return result;
}
