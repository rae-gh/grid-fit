# Basic integration test for gridfit Python binding
import gridfit

def test_interp():
    result = gridfit.interp(0, 1, 1)
    assert result == [0.5], f"Expected [0.5], got {result}"
