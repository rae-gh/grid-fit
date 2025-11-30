#include "gridfit.h"
#include "alcraft_matrices.h"
#include <stdexcept>

GridFit::GridFit(const std::vector<float> &x, const std::vector<float> &y,
                 const std::vector<float> &z, const std::vector<float> &values,
                 int order)
    : x_(x), y_(y), z_(z), values_(values), order_(order) {

  if (order == 2) {
    matrix_ = alcraft::TRILINEAR_MATRIX;
    matrix_size_ = 8;
  } else if (order == 3) {
    matrix_ = alcraft::TRICUBIC_MATRIX;
    matrix_size_ = 64;
  } else {
    throw std::invalid_argument("Order must be 2 or 3");
  }
}

std::string GridFit::details() {
  return "GridFit order: " + std::to_string(order_);
}

std::vector<float> GridFit::interpolate(const std::vector<float> &points,
                                        int n_points, int ndim) {
  std::vector<float> result;
  result.resize(n_points, 0.0f);
  int nx = x_.size();
  int ny = y_.size();
  int nz = z_.size();
  for (int i = 0; i < n_points; ++i) {
    float px = points[i * ndim + 0];
    float py = points[i * ndim + 1];
    float pz = points[i * ndim + 2];

    // Find lower and upper indices for each axis
    int ix = 0, iy = 0, iz = 0;
    while (ix + 1 < nx && x_[ix + 1] <= px)
      ++ix;
    while (iy + 1 < ny && y_[iy + 1] <= py)
      ++iy;
    while (iz + 1 < nz && z_[iz + 1] <= pz)
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
              values_[(ix + dx) * ny * nz + (iy + dy) * nz + (iz + dz)];

    // Matrix Mult between corners and the const matrix
    float out[8] = {0};
    for (int row = 0; row < 8; ++row) {
      for (int col = 0; col < 8; ++col) {
        out[row] += matrix_[row * 8 + col] * corner_values[col];
      }
    }

    float mout[2][2][2];
    idx = 0;
    for (int i1 = 0; i1 <= 1; ++i1)
      for (int j1 = 0; j1 <= 1; ++j1)
        for (int k1 = 0; k1 <= 1; ++k1)
          mout[i1][j1][k1] = out[idx++];

    float dpx = px - x_[ix];
    float dpy = py - y_[iy];
    float dpz = pz - z_[iz];

    float fx[2] = {1.0f, dpx};
    float fy[2] = {1.0f, dpy};
    float fz[2] = {1.0f, dpz};

    // Precompute all 8 products of fx, fy, fz
    float prod[8];
    int pidx = 0;
    for (int i1 = 0; i1 <= 1; ++i1)
      for (int j1 = 0; j1 <= 1; ++j1)
        for (int k1 = 0; k1 <= 1; ++k1)
          prod[pidx++] = fx[i1] * fy[j1] * fz[k1];

    // Unroll the interpolation sum
    float px_interp = 0.0f;
    for (int idxu = 0; idxu < 8; ++idxu) {
      px_interp += mout[idxu / 4][(idxu / 2) % 2][idxu % 2] * prod[idxu];
    }
    result[i] = px_interp;
  }
  return result;
}
