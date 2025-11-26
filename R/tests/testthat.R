library(testthat)
library(gridfitInterp)

test_that("interp works", {
  expect_equal(interp(0, 1, 1), 0.5)
})
