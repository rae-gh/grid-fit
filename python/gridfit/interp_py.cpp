#include <Python.h>
#include "../include/interp.h"
#include <vector>

static PyObject* py_interp(PyObject* self, PyObject* args) {
    float a, b;
    int n;
    if (!PyArg_ParseTuple(args, "ffi", &a, &b, &n))
        return NULL;
    std::vector<float> result = interp(a, b, n);
    PyObject* pylist = PyList_New(result.size());
    for (size_t i = 0; i < result.size(); ++i) {
        PyList_SetItem(pylist, i, PyFloat_FromDouble(result[i]));
    }
    return pylist;
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
    return PyModule_Create(&moduledef);
}
