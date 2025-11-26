cmake_minimum_required(VERSION 3.10)
project(gridfit_test_interp)

# Add include directory
include_directories(${CMAKE_SOURCE_DIR}/../../include)

# Add executable
add_executable(test_interp test_interp.cpp ../../src/interp.cpp)