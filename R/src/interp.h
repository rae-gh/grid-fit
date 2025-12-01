#pragma once
#include <vector>


std::vector<float> interp(double a, double b, int n);

// Dummy trilinear interpolation function (flat points)
// points: flat vector of size n_points * ndim (row-major)
std::vector<float> trilinear(
	const std::vector<float>& x,
	const std::vector<float>& y,
	const std::vector<float>& z,
	const std::vector<float>& values,
	const std::vector<float>& points,
	int n_points,
	int ndim
);
