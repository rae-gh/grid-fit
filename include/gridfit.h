#pragma once
#include <string>
#include <vector>

class GridFit {
private:
  // Grid definition
  std::vector<float> x_;
  std::vector<float> y_;
  std::vector<float> z_;
  std::vector<float> values_;

  // Interpolation settings
  int order_;
  const float *matrix_;
  int matrix_size_;

public:
  // Constructor takes grid data and order
  GridFit(const std::vector<float> &x, const std::vector<float> &y,
          const std::vector<float> &z, const std::vector<float> &values,
          int order = 3);

  // Interpolate at given points
  std::vector<float> interpolate(const std::vector<float> &points, int n_points,
                                 int ndim);

  std::string details();
};