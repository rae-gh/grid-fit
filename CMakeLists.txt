cmake_minimum_required(VERSION 3.10)
project(gridfit_interp)

add_library(gridfit_interp SHARED src/interp.cpp)

target_include_directories(gridfit_interp PUBLIC ${PROJECT_SOURCE_DIR}/include)
