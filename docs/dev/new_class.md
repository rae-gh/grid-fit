# Adding a New C++ Class to gridfit with pybind11

## Step-by-step Guide

### 1. Create the Header File
**File:** `include/your_class.h`
```cpp
#pragma once
#include <string>
#include <vector>

class YourClass {
private:
    // Private member variables
    std::vector<float> data_;
    
public:
    // Constructor
    YourClass();
    
    // Methods
    std::string details();
    void someMethod(int param);
};
```

### 2. Create the Implementation File
**File:** `src/your_class.cpp`
```cpp
#include "your_class.h"

YourClass::YourClass() {
    // Constructor implementation
}

std::string YourClass::details() {
    return "Implementation here";
}

void YourClass::someMethod(int param) {
    // Method implementation
}
```

### 3. Update the Python Bindings
**File:** `python/gridfit/interp_py.cpp`

**Add include at top:**
```cpp
#include "../include/your_class.h"
```

**Add to `PYBIND11_MODULE` section:**
```cpp
PYBIND11_MODULE(gridfit_interp, m) {
    // ... existing bindings ...
    
    // Bind your new class
    py::class_<YourClass>(m, "YourClass")
        .def(py::init<>())                          // Constructor with no args
        .def("details", &YourClass::details)        // Bind method
        .def("some_method", &YourClass::someMethod, // Bind method with args
             py::arg("param"));
}
```

### 4. Update setup.py
**File:** `setup.py`

Add the new source file to the sources list:
```python
ext_modules = [
    Pybind11Extension(
        "gridfit.gridfit_interp",
        sources=[
            "python/gridfit/interp_py.cpp", 
            "src/interp.cpp",
            "src/your_class.cpp"  # ADD THIS
        ],
        include_dirs=["include"],
        language="c++",
        cxx_std=11,
    ),
]
```

### 5. Update Python Package Init
**File:** `python/gridfit/__init__.py`

Expose the class to Python users:
```python
from .gridfit_interp import YourClass
```

### 6. Build and Install
```bash
# Clean previous build
rm -rf build/

# Reinstall
pip install -e .
```

### 7. Test from Python
```python
from gridfit import YourClass

obj = YourClass()
print(obj.details())
```

---

## Common Patterns

### Constructor with Parameters
```cpp
// C++ header
YourClass(int size, double value);

// pybind11 binding
.def(py::init<int, double>(),
     py::arg("size"), py::arg("value"))
```

### Method Returning NumPy Array
```cpp
// C++ method
std::vector<float> getData();

// pybind11 binding
.def("get_data", [](YourClass& self) {
    std::vector<float> data = self.getData();
    return py::array_t<float>(data.size(), data.data());
})
```

### Method Taking NumPy Array
```cpp
// C++ wrapper in interp_py.cpp
void setData_wrapper(YourClass& self, py::array_t<float> arr) {
    auto buf = arr.request();
    std::vector<float> vec(static_cast<float*>(buf.ptr),
                           static_cast<float*>(buf.ptr) + buf.size);
    self.setData(vec);
}

// pybind11 binding
.def("set_data", &setData_wrapper)
```

---

## Checklist

- [ ] Created `include/your_class.h`
- [ ] Created `src/your_class.cpp`
- [ ] Added `#include` to `interp_py.cpp`
- [ ] Added `py::class_<>` binding to `PYBIND11_MODULE`
- [ ] Added source file to `setup.py`
- [ ] Exposed class in `__init__.py`
- [ ] Rebuilt with `pip install -e .`
- [ ] Tested from Python

---

## Troubleshooting

**"undefined symbol" error:**
- Check that `.cpp` file is in `setup.py` sources
- Rebuild with `rm -rf build/ && pip install -e .`

**"cannot import name" error:**
- Check class is exposed in `__init__.py`
- Check binding name matches: `py::class_<YourClass>(m, "YourClass")`

**Build errors:**
- Check all includes are correct
- Check `#pragma once` in header
- Check constructor/method signatures match between `.h` and `.cpp`