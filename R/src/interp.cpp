#include <Rcpp.h>
#include "../../include/interp.h"
using namespace Rcpp;

// [[Rcpp::export]]
NumericVector interp(double a, double b, int n) {
    std::vector<float> res = ::interp(a, b, n);
    NumericVector out(res.begin(), res.end());
    return out;
}
