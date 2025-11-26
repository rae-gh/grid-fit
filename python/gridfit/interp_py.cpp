
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>
#include "../include/interp.h"
#include <vector>
#include <stdexcept>

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


// Helper: Convert 1D numpy array to std::vector<float>
static std::vector<float> pyarray_to_vector(PyObject* arr) {
    PyArrayObject* np_arr = (PyArrayObject*)PyArray_FROM_OTF(arr, NPY_FLOAT, NPY_ARRAY_IN_ARRAY);
    if (!np_arr) throw std::runtime_error("Failed to convert numpy array");
    float* data = static_cast<float*>(PyArray_DATA(np_arr));
    npy_intp n = PyArray_SIZE(np_arr);
    std::vector<float> vec(data, data + n);
    Py_DECREF(np_arr);
    return vec;
}


// Helper: Convert 2D numpy array to flat std::vector<float> and get shape
static std::vector<float> pyarray2d_to_flatvec(PyObject* arr, npy_intp& nrow, npy_intp& ncol) {
    PyArrayObject* np_arr = (PyArrayObject*)PyArray_FROM_OTF(arr, NPY_FLOAT, NPY_ARRAY_IN_ARRAY);
    if (!np_arr) throw std::runtime_error("Failed to convert numpy array");
    int nd = PyArray_NDIM(np_arr);
    if (nd != 2) throw std::runtime_error("points must be 2D array");
    npy_intp* dims = PyArray_DIMS(np_arr);
    nrow = dims[0];
    ncol = dims[1];
    float* data = static_cast<float*>(PyArray_DATA(np_arr));
    std::vector<float> out(data, data + nrow * ncol);
    Py_DECREF(np_arr);
    return out;
}

static PyObject* py_trilinear(PyObject* self, PyObject* args) {
    PyObject *x_obj, *y_obj, *z_obj, *values_obj, *points_obj;
    if (!PyArg_ParseTuple(args, "OOOOO", &x_obj, &y_obj, &z_obj, &values_obj, &points_obj))
        return NULL;
    try {
        std::vector<float> x = pyarray_to_vector(x_obj);
        std::vector<float> y = pyarray_to_vector(y_obj);
        std::vector<float> z = pyarray_to_vector(z_obj);
        std::vector<float> values = pyarray_to_vector(values_obj);
        npy_intp nrow, ncol;
        std::vector<float> points_flat = pyarray2d_to_flatvec(points_obj, nrow, ncol);
        std::vector<float> result = trilinear(x, y, z, values, points_flat, static_cast<int>(nrow), static_cast<int>(ncol));
        npy_intp dims[1] = { static_cast<npy_intp>(result.size()) };
        PyObject* array = PyArray_SimpleNew(1, dims, NPY_FLOAT);
        if (!array) return NULL;
        float* array_data = static_cast<float*>(PyArray_DATA((PyArrayObject*)array));
        std::copy(result.begin(), result.end(), array_data);
        return array;
    } catch (const std::exception& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}

static PyMethodDef Methods[] = {
    {"interp", py_interp, METH_VARARGS, "Linear interpolation."},
    {"trilinear", py_trilinear, METH_VARARGS, "Dummy trilinear interpolation (returns 42.0 for each point)."},
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
