#pragma once
#include <string>
#include <vector>

class GridFit {
private:
  // Store pointers to data instead of copies
  const float *x_data_;
  const float *y_data_;
  const float *z_data_;
  const float *values_data_;

  // Store sizes
  size_t nx_, ny_, nz_;

  // Interpolation settings
  int order_;
  const float *matrix_;
  int matrix_size_;

public:
  // Constructor takes pointers and sizes
  GridFit(const float *x, size_t nx, const float *y, size_t ny, const float *z,
          size_t nz, const float *values, int order = 2);

  // Interpolate at given points
  std::vector<float> interpolate(const std::vector<float> &points, int n_points,
                                 int ndim);

  std::string details();
};