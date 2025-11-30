





Target interface
# Simple drop-in for scipy users:
from gridfit import RegularGrid3D

grid = RegularGrid3D(data, spacing=(1.0, 1.0, 2.5))  # voxel sizes
values = grid.interpolate(points, method='trilinear')  # scipy-like
slice_img = grid.slice_through_points(p1, p2, p3)  # your feature
projection = grid.project(axis='z')  # your feature