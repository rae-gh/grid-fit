#!/bin/bash
# benchmark.sh - Run all grid-fit benchmarks
# benchmarks/benchmark.sh
set -e

# Find and run all Python benchmark scripts in this directory
shopt -s nullglob
for f in "$(dirname "$0")"/*.py; do
    fname=$(basename "$f")
    echo "--- Running $fname ---"
    python "$f" "$@"
    echo "--- End of $fname ---"
done
shopt -u nullglob
