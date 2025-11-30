#include "gridfit.h"
#include "alcraft_matrices.h"
#include <algorithm>
#include <stdexcept>

GridFit::GridFit(const float *x, size_t nx, const float *y, size_t ny,
                 const float *z, size_t nz, const float *values, int order)
    : x_data_(x), nx_(nx), y_data_(y), ny_(ny), z_data_(z), nz_(nz),
      values_data_(values), order_(order) {

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
  return "GridFit order: " + std::to_string(order_) +
         ", grid: " + std::to_string(nx_) + "×" + std::to_string(ny_) + "×" +
         std::to_string(nz_);
}

std::vector<float> GridFit::interpolate(const std::vector<float> &points,
                                        int n_points, int ndim) {
  std::vector<float> result(n_points, 0.0f);

  for (int i = 0; i < n_points; ++i) {
    float px = points[i * ndim + 0];
    float py = points[i * ndim + 1];
    float pz = points[i * ndim + 2];

    // Binary search using pointers
    auto find_index = [](const float *arr, size_t n, float val) -> int {
      auto it = std::upper_bound(arr, arr + n, val);
      int idx = std::max(0, (int)(it - arr - 1));
      return std::min(idx, (int)n - 2);
    };

    int ix = find_index(x_data_, nx_, px);
    int iy = find_index(y_data_, ny_, py);
    int iz = find_index(z_data_, nz_, pz);

    // Rest of interpolation stays the same, but use pointers
    float corner_values[8];
    int idx = 0;
    for (int dx = 0; dx <= 1; ++dx)
      for (int dy = 0; dy <= 1; ++dy)
        for (int dz = 0; dz <= 1; ++dz)
          corner_values[idx++] =
              values_data_[(ix + dx) * ny_ * nz_ + (iy + dy) * nz_ + (iz + dz)];

    // Matrix multiplication
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

    float dpx = px - x_data_[ix];
    float dpy = py - y_data_[iy];
    float dpz = pz - z_data_[iz];

    float fx[2] = {1.0f, dpx};
    float fy[2] = {1.0f, dpy};
    float fz[2] = {1.0f, dpz};

    float prod[8];
    int pidx = 0;
    for (int i1 = 0; i1 <= 1; ++i1)
      for (int j1 = 0; j1 <= 1; ++j1)
        for (int k1 = 0; k1 <= 1; ++k1)
          prod[pidx++] = fx[i1] * fy[j1] * fz[k1];

    float px_interp = 0.0f;
    for (int idxu = 0; idxu < 8; ++idxu) {
      px_interp += mout[idxu / 4][(idxu / 2) % 2][idxu % 2] * prod[idxu];
    }
    result[i] = px_interp;
  }
  return result;
}