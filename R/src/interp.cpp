#include <vector>
#include <Rcpp.h>
#include "interp.h"
using namespace Rcpp;

// [[Rcpp::export(name = interp_rcpp)]]
NumericVector interp_rcpp(double a, double b, int n) {
    std::vector<float> res = ::interp(a, b, n);
    NumericVector out(res.begin(), res.end());
    return out;
}
// [[Rcpp::export(name = trilinear_rcpp)]]
Rcpp::NumericVector trilinear_rcpp(Rcpp::NumericVector x, Rcpp::NumericVector y, Rcpp::NumericVector z, Rcpp::NumericVector values, Rcpp::NumericMatrix points) {
    std::vector<float> xvec(x.begin(), x.end());
    std::vector<float> yvec(y.begin(), y.end());
    std::vector<float> zvec(z.begin(), z.end());
    std::vector<float> valuesvec(values.begin(), values.end());
    // Flatten points matrix to a single vector (row-major)
    std::vector<float> pts;
    pts.reserve(points.nrow() * points.ncol());
    for (int i = 0; i < points.nrow(); ++i) {
        for (int j = 0; j < points.ncol(); ++j) {
            pts.push_back(static_cast<float>(points(i, j)));
        }
    }
    int n_points = points.nrow();
    int n_dim = points.ncol();
    std::vector<float> res = ::trilinear(xvec, yvec, zvec, valuesvec, pts, n_points, n_dim);
    Rcpp::NumericVector out(res.begin(), res.end());
    return out;
}