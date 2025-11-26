
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>
#include "../include/interp.h"
#include <vector>

static PyObject* py_interp(PyObject* self, PyObject* args) {
    float a, b;
    int n;
    if (!PyArg_ParseTuple(args, "ffi", &a, &b, &n))
        return NULL;
    std::vector<float> result = interp(a, b, n);
    npy_intp dims[1] = { static_cast<npy_intp>(result.size()) };
    PyObject* array = PyArray_SimpleNew(1, dims, NPY_FLOAT);
    if (!array) return NULL;
    float* array_data = static_cast<float*>(PyArray_DATA((PyArrayObject*)array));
    std::copy(result.begin(), result.end(), array_data);
    return array;
}

static PyMethodDef Methods[] = {
    {"interp", py_interp, METH_VARARGS, "Linear interpolation."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "gridfit_interp",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_gridfit_interp(void) {
    import_array(); // Initialize numpy C API
    return PyModule_Create(&moduledef);
}
