#define NOT_MAIN 1

#include "xdelta3.h"
#include "xdelta3.c"
#include <Python.h>

static PyObject *XDeltaDeltaTooBig;
static PyObject *XDeltaError;

static PyObject * xdelta3_encode_decode(PyObject *self, PyObject *args)
{
    uint8_t *input_bytes = NULL, *source_bytes = NULL, *output_buf = NULL;
    int input_len, source_len, flags, action, result;
    size_t input_size, source_size, output_alloc, output_size;

    if (!PyArg_ParseTuple(args, "y#y#ii", &input_bytes, &input_len, &source_bytes, &source_len, &flags, &action))
        return NULL;

    source_size = (size_t)source_len;
    input_size = (size_t)input_len;


    if (action == 0) {
        output_alloc = input_size;
        output_buf = main_malloc(output_alloc);
        result = xd3_encode_memory(input_bytes, input_size, source_bytes, source_size,
                output_buf, &output_size, output_alloc, flags);
    } else {
        output_alloc = input_size  * 100; // TODO
        output_buf = main_malloc(output_alloc);
        result = xd3_decode_memory(input_bytes, input_size, source_bytes, source_size,
                output_buf, &output_size, output_alloc, flags);
    }

    if (result != 0) {
        if(result == ENOSPC) {
            PyErr_SetString(XDeltaDeltaTooBig, "delta too big: ENOSPC");
        } else {
            PyErr_SetString(XDeltaError, xd3_strerror(result));
        }
        return NULL;
    }

    return Py_BuildValue("y#", output_buf, output_size);
}

static PyMethodDef xdelta3_methods[] = {
    {"encode_decode",  xdelta3_encode_decode, METH_VARARGS, "xdelta3 encode or decode"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef xdelta3_module = {
   PyModuleDef_HEAD_INIT,
   "xdelta3",   /* name of module */
   "xdelta3", /* module documentation, may be NULL */
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

    XDeltaDeltaTooBig = PyErr_NewException("xdelta3.XDeltaDeltaTooBig", NULL, NULL);
    Py_INCREF(XDeltaDeltaTooBig);
    PyModule_AddObject(m, "error", XDeltaDeltaTooBig);
    return m;
}
