#include <Rcpp.h>
#include "interp.h"
using namespace Rcpp;

// [[Rcpp::export(name = interp_rcpp)]]
NumericVector interp_rcpp(double a, double b, int n) {
    std::vector<float> res = ::interp(a, b, n);
    NumericVector out(res.begin(), res.end());
    return out;
}
