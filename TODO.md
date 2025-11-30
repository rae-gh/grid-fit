# Target interface - PYTHON
## Simple drop-in for scipy users:
from gridfit import RegularGrid3D

grid = RegularGrid3D(data, spacing=(1.0, 1.0, 2.5))  # voxel sizes
values = grid.interpolate(points, method='trilinear')  # scipy-like
slice_img = grid.slice_through_points(p1, p2, p3)  # your feature
projection = grid.project(axis='z')  # your feature

# Target interface - R

library(gridfit)
# Create grid
grid <- GridFit(data_array, spacing = c(1.0, 1.0, 2.5), order = 3)
# Slice through 3 points
slice <- grid$slice_through_points(p1, p2, p3)
# Or convenience methods
slice <- grid$slice_at_angle(axis = "z", angle = 30, offset = 10)

### Bioconductor package potential:
- Submit to Bioconductor (R's biology package repo)
- Paper in Bioinformatics or similar
- Actually gets used/cited
The work to add R support:
- You already have the C++ core
- Rcpp bindings (similar effort to pybind11)
- R package structure (DESCRIPTION, NAMESPACE, etc.)
- Documentation/vignettes