#include <iostream>
#include <vector>
#include <chrono>
#include "../../include/interp.h"

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    float x0 = 0.0f, x1 = 1.0f;
    int n = 10000;
    std::vector<float> result = interp(x0, x1, n);

    std::cout << "interp(" << x0 << ", " << x1 << ", " << n << ") = [";
    for (size_t i = 0; i < result.size(); ++i) {
        std::cout << result[i];
        if (i + 1 < result.size()) std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Total time: " << elapsed.count() << " seconds" << std::endl;

    return 0;
}
