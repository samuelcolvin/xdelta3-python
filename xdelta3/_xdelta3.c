#define NOT_MAIN 1

#include "xdelta3.h"
#include "xdelta3.c"
#include <Python.h>

static PyObject *XDeltaNotPossible;
static PyObject *XDeltaError;

static PyObject * xdelta3_encode(PyObject *self, PyObject *args)
{
    uint8_t *before_bytes = NULL, *after_bytes = NULL, *delta_buf = NULL;
    int before_len, after_len;
    size_t before_size, after_size, delta_alloc;
    size_t delta_size;

    if (!PyArg_ParseTuple(args, "y#y#", &before_bytes, &before_len, &after_bytes, &after_len))
        return NULL;

    int flags = XD3_COMPLEVEL_9;

    before_size = (size_t)before_len;
    after_size = (size_t)after_len;

    delta_alloc = after_size * 11 / 10;
    delta_buf = main_malloc(delta_alloc);

//    fprintf(stderr, "before len: %d %d\n", before_len, (int)before_size);
//    fprintf(stderr, "after len: %d %d\n", after_len, (int)after_size);
//    fprintf(stderr, "delta_alloc: %d\n", (int)delta_alloc);

    int ret = xd3_encode_memory(after_bytes, after_size, before_bytes, before_size,
            delta_buf, &delta_size, delta_alloc, flags);

    if (ret != 0) {
        if(ret == 28) {
            // seems to be a special case for "can't delta"
            PyErr_SetString(XDeltaNotPossible, "no delta possible");
        } else {
            char exc_str[80];
            sprintf(exc_str, "%d %s", ret, xd3_strerror(ret));
            PyErr_SetString(XDeltaError, exc_str);
        }
        return NULL;
    }

    return Py_BuildValue("y", delta_buf);
}

static PyMethodDef xdelta3_methods[] = {
    {"encode",  xdelta3_encode, METH_VARARGS, "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef xdelta3_module = {
   PyModuleDef_HEAD_INIT,
   "xdelta3",   /* name of module */
   "this is xdelta3", /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
   xdelta3_methods
};

PyMODINIT_FUNC PyInit__xdelta3(void) {
    PyObject *m;

    m = PyModule_Create(&xdelta3_module);
    if (m == NULL)
        return NULL;

    XDeltaError = PyErr_NewException("xdelta3.XDeltaError", NULL, NULL);
    Py_INCREF(XDeltaError);
    PyModule_AddObject(m, "error", XDeltaError);

    XDeltaNotPossible = PyErr_NewException("xdelta3.XDeltaNotPossible", NULL, NULL);
    Py_INCREF(XDeltaNotPossible);
    PyModule_AddObject(m, "error", XDeltaNotPossible);
    return m;
}
