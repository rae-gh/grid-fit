#include "../include/gridfit.h"
#include "../include/interp.h"
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// Wrapper for trilinear that handles numpy arrays
py::array_t<float> py_trilinear(py::array_t<float> x, py::array_t<float> y,
                                py::array_t<float> z, py::array_t<float> values,
                                py::array_t<float> points) {
  auto x_buf = x.request();
  auto y_buf = y.request();
  auto z_buf = z.request();
  auto values_buf = values.request();
  auto points_buf = points.request();

  if (points_buf.ndim != 2) {
    throw std::runtime_error("points must be 2D array");
  }

  int nrow = points_buf.shape[0];
  int ncol = points_buf.shape[1];

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

  std::vector<float> result =
      trilinear(x_vec, y_vec, z_vec, values_vec, points_vec, nrow, ncol);

  return py::array_t<float>(result.size(), result.data());
}

PYBIND11_MODULE(gridfit_interp, m) {
  m.doc() = "Grid interpolation module";

  m.def("interp", &interp, "Linear interpolation", py::arg("a"), py::arg("b"),
        py::arg("n"));

  m.def("trilinear", &py_trilinear, "Trilinear interpolation", py::arg("x"),
        py::arg("y"), py::arg("z"), py::arg("values"), py::arg("points"));

  // GridFit class with lambda constructor for efficient numpy handling
  py::class_<GridFit>(m, "GridFit")
      .def(py::init([](py::array_t<float> x, py::array_t<float> y,
                       py::array_t<float> z, py::array_t<float> values,
                       int order) {
             // Get buffer info
             auto x_buf = x.request();
             auto y_buf = y.request();
             auto z_buf = z.request();
             auto values_buf = values.request();

             // Convert directly from numpy buffers to vectors (1 copy each)
             std::vector<float> x_vec(static_cast<float *>(x_buf.ptr),
                                      static_cast<float *>(x_buf.ptr) +
                                          x_buf.size);
             std::vector<float> y_vec(static_cast<float *>(y_buf.ptr),
                                      static_cast<float *>(y_buf.ptr) +
                                          y_buf.size);
             std::vector<float> z_vec(static_cast<float *>(z_buf.ptr),
                                      static_cast<float *>(z_buf.ptr) +
                                          z_buf.size);
             std::vector<float> values_vec(
                 static_cast<float *>(values_buf.ptr),
                 static_cast<float *>(values_buf.ptr) + values_buf.size);

             return new GridFit(x_vec, y_vec, z_vec, values_vec, order);
           }),
           py::arg("x"), py::arg("y"), py::arg("z"), py::arg("values"),
           py::arg("order") = 2,
           "Create GridFit interpolator\n\n"
           "Args:\n"
           "    x: X-axis grid coordinates (1D array)\n"
           "    y: Y-axis grid coordinates (1D array)\n"
           "    z: Z-axis grid coordinates (1D array)\n"
           "    values: Grid values (can be 3D array - will be flattened "
           "automatically)\n"
           "    order: 2 for trilinear (default), 3 for tricubic")
      .def(
          "interpolate",
          [](GridFit &self, py::array_t<float> points) {
            auto points_buf = points.request();

            int n_points, ndim;
            if (points_buf.ndim == 2) {
              n_points = points_buf.shape[0];
              ndim = points_buf.shape[1];
            } else if (points_buf.ndim == 1) {
              n_points = 1;
              ndim = points_buf.size;
            } else {
              throw std::runtime_error("points must be 1D or 2D array");
            }

            std::vector<float> points_vec(static_cast<float *>(points_buf.ptr),
                                          static_cast<float *>(points_buf.ptr) +
                                              points_buf.size);

            std::vector<float> result =
                self.interpolate(points_vec, n_points, ndim);

            return py::array_t<float>(result.size(), result.data());
          },
          py::arg("points"), "Interpolate at given points")
      .def("details", &GridFit::details);
}