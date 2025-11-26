#include "interp.h"
#include <cstdio>
#include <vector>

std::vector<float> interp(double a, double b, int n) {
  std::vector<float> result;
  if (n <= 0)
    return result;
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
std::vector<float>
trilinear(const std::vector<float> &x, const std::vector<float> &y,
          const std::vector<float> &z, const std::vector<float> &values,
          const std::vector<float> &points, int n_points, int ndim) {
  std::vector<float> result;
  result.resize(n_points, 0.0f); // Dummy value
  int nx = x.size();
  int ny = y.size();
  int nz = z.size();
  for (int i = 0; i < n_points; ++i) {
    float px = points[i * ndim + 0];
    float py = points[i * ndim + 1];
    float pz = points[i * ndim + 2];
    printf("Point %d: (%.4f, %.4f, %.4f)\n", i, px, py, pz);

    // Find lower and upper indices for each axis
    int ix = 0, iy = 0, iz = 0;
    while (ix + 1 < nx && x[ix + 1] <= px)
      ++ix;
    while (iy + 1 < ny && y[iy + 1] <= py)
      ++iy;
    while (iz + 1 < nz && z[iz + 1] <= pz)
      ++iz;
    int ixu = (ix + 1 < nx) ? ix + 1 : ix;
    int iyu = (iy + 1 < ny) ? iy + 1 : iy;
    int izu = (iz + 1 < nz) ? iz + 1 : iz;

    printf("  x: lower=%.4f upper=%.4f\n", x[ix], x[ixu]);
    printf("  y: lower=%.4f upper=%.4f\n", y[iy], y[iyu]);
    printf("  z: lower=%.4f upper=%.4f\n", z[iz], z[izu]);

    result[i] = 42.0f; // Still dummy
  }
  return result;
}
