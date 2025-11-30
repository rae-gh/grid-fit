#include "interp.h"
#include <cmath>
#include <cstdio>
#include <vector>

// Hard-coded 8x8 matrix (row-major, all zeros)
// clang-format off
const float mat[64] = {
     1., 0., 0., 0., 0., 0., 0., 0., 
    -1., 1., 0., 0., 0., 0., 0., 0.,
    -1., 0., 1., 0., 0., 0., 0., 0., 
     1.,-1.,-1., 1., 0., 0., 0., 0.,
    -1., 0., 0., 0., 1., 0., 0., 0., 
     1.,-1., 0., 0.,-1., 1., 0., 0.,
     1., 0.,-1., 0.,-1., 0., 1., 0., 
    -1., 1., 1.,-1., 1.,-1.,-1., 1.};
// clang-format on

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

std::vector<float>
trilinear(const std::vector<float> &x, const std::vector<float> &y,
          const std::vector<float> &z, const std::vector<float> &values,
          const std::vector<float> &points, int n_points, int ndim) {
  std::vector<float> result;
  result.resize(n_points, 0.0f);
  int nx = x.size();
  int ny = y.size();
  int nz = z.size();
  for (int i = 0; i < n_points; ++i) {
    float px = points[i * ndim + 0];
    float py = points[i * ndim + 1];
    float pz = points[i * ndim + 2];

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

    float corner_values[8];
    int idx = 0;
    for (int dx = 0; dx <= 1; ++dx)
      for (int dy = 0; dy <= 1; ++dy)
        for (int dz = 0; dz <= 1; ++dz)
          corner_values[idx++] =
              values[(ix + dx) * ny * nz + (iy + dy) * nz + (iz + dz)];

    // Matrix Mult between corners and the const matrix
    float out[8] = {0};
    for (int row = 0; row < 8; ++row) {
      for (int col = 0; col < 8; ++col) {
        out[row] += mat[row * 8 + col] * corner_values[col];
      }
    }

    float dpx = px - x[ix];
    float dpy = py - y[iy];
    float dpz = pz - z[iz];

    float px_interp = 0.0f;
    idx = 0;
    for (int i1 = 0; i1 <= 1; ++i1)
      for (int j1 = 0; j1 <= 1; ++j1)
        for (int k1 = 0; k1 <= 1; ++k1) {
          float coeff = out[idx++];
          float fx = (i1 == 0) ? 1.0f : dpx;
          float fy = (j1 == 0) ? 1.0f : dpy;
          float fz = (k1 == 0) ? 1.0f : dpz;
          px_interp += coeff * fx * fy * fz;
        }
    result[i] = px_interp;
  }
  return result;
}
