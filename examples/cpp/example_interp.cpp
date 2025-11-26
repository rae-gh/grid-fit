// Example usage of the gridfit C++ core
#include <iostream>
#include <vector>
#include <chrono>
#include "../../include/interp.h"

int main() {
    int n = 10000000;
    // Warm up
    auto warmup = interp(0.0, 1.0, n);

    auto start = std::chrono::high_resolution_clock::now();
    auto result = interp(0.0, 1.0, n);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    if (!result.empty()) {
        std::cout << "n: " << result.size()
                  << ", First: " << result.front()                  
                  << ", Last: " << result.back() << std::endl;
    } else {
        std::cout << "No points returned." << std::endl;
    }
    std::cout << "Time taken: " << elapsed.count() << " seconds" << std::endl;
    return 0;
}
