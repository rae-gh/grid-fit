# /bin/bash

# Run this to test the Python and R bindings for gridfit

# examples/bash/interp.sh

echo "---------------------------------------"
echo "Testing gridfit Python and R bindings..."
echo "---------------------------------------"
echo "Python example output:"
python examples/python/example_interp.py
echo "---------------------------------------"
echo "R example output:"
Rscript examples/R/example_interp.R
echo "---------------------------------------"
echo "C++ example output:" 
./examples/cpp/example_interp
echo "---------------------------------------"
