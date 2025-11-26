#include <iostream>
#include <vector>
#include <chrono>
#include "../../include/interp.h"

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    float x0 = 0.0f, x1 = 1.0f;
    int n = 10000000;
    std::vector<float> result = interp(x0, x1, n);

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    if (!result.empty()) {
        std::cout << "First: " << result.front() << ", Last: " << result.back() << ", Count: " << result.size() << std::endl;
    } else {
        std::cout << "No points returned." << std::endl;
    }
    std::cout << "Total time: " << elapsed.count() << " seconds" << std::endl;
    return 0;
}
