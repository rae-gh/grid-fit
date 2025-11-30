#include "../include/interp.h"
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// Wrapper for trilinear that handles numpy arrays
py::array_t<float> py_trilinear(py::array_t<float> x, py::array_t<float> y,
                                py::array_t<float> z, py::array_t<float> values,
                                py::array_t<float> points) {
  // Get buffer info for easy access
  auto x_buf = x.request();
  auto y_buf = y.request();
  auto z_buf = z.request();
  auto values_buf = values.request();
  auto points_buf = points.request();

  // Check points is 2D
  if (points_buf.ndim != 2) {
    throw std::runtime_error("points must be 2D array");
  }

  int nrow = points_buf.shape[0];
  int ncol = points_buf.shape[1];

  // Convert to vectors (pybind11 can do this automatically with py::stl,
  // but showing explicit conversion for clarity)
  std::vector<float> x_vec(static_cast<float *>(x_buf.ptr),
                           static_cast<float *>(x_buf.ptr) + x_buf.size);
  std::vector<float> y_vec(static_cast<float *>(y_buf.ptr),
                           static_cast<float *>(y_buf.ptr) + y_buf.size);
  std::vector<float> z_vec(static_cast<float *>(z_buf.ptr),
                           static_cast<float *>(z_buf.ptr) + z_buf.size);
  std::vector<float> values_vec(static_cast<float *>(values_buf.ptr),
                                static_cast<float *>(values_buf.ptr) +
                                    values_buf.size);
  std::vector<float> points_vec(static_cast<float *>(points_buf.ptr),
                                static_cast<float *>(points_buf.ptr) +
                                    points_buf.size);

  // Call your C++ function
  std::vector<float> result =
      trilinear(x_vec, y_vec, z_vec, values_vec, points_vec, nrow, ncol);

  // Return as numpy array (pybind11 handles conversion automatically!)
  return py::array_t<float>(result.size(), result.data());
}

PYBIND11_MODULE(gridfit_interp, m) {
  m.doc() = "Grid interpolation module";

  // Bind the simple interp function directly - pybind11 handles vector
  // conversion!
  m.def("interp", &interp, "Linear interpolation", py::arg("a"), py::arg("b"),
        py::arg("n"));

  // Bind the trilinear wrapper
  m.def("trilinear", &py_trilinear, "Trilinear interpolation", py::arg("x"),
        py::arg("y"), py::arg("z"), py::arg("values"), py::arg("points"));
}