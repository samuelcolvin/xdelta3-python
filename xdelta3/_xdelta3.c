#define NOT_MAIN 1

#include "xdelta3.h"
#include "xdelta3.c"
#include <Python.h>

static PyObject * xdelta3_execute(PyObject *self, PyObject *args)
{
  uint8_t *input_bytes = NULL, *source_bytes = NULL, *output_buf = NULL;
  int input_len, source_len, flags, action, result;
  size_t input_size, source_size, output_alloc, output_size;

  if (!PyArg_ParseTuple(args, "y#y#ii", &input_bytes, &input_len, &source_bytes, &source_len, &flags, &action))
    return NULL;

  source_size = (size_t)source_len;
  input_size = (size_t)input_len;

  if (action == 0) {
    // if the output would be longer than the input itself, there's no point using delta encoding
    output_alloc = input_size;
    output_buf = main_malloc(output_alloc);
    result = xd3_encode_memory(input_bytes, input_size, source_bytes, source_size,
        output_buf, &output_size, output_alloc, flags);
  } else {
    // output shouldn't be bigger than the original plus the delta, but give a little leeway
    output_alloc = input_size + source_size * 11 / 10;
    output_buf = main_malloc(output_alloc);
    result = xd3_decode_memory(input_bytes, input_size, source_bytes, source_size,
        output_buf, &output_size, output_alloc, flags);
  }

  if (result == 0) {
    PyObject *ret = Py_BuildValue("y#", output_buf, output_size);
    main_free(output_buf);
    return ret;
  }

  if(result == ENOSPC) {
    PyErr_SetString(PyExc_RuntimeError, "ENOSPC");
  } else {
    PyErr_SetString(PyExc_RuntimeError, xd3_strerror(result));
  }
  main_free(output_buf);
  return NULL;
}

static PyMethodDef xdelta3_methods[] = {
  {"execute",  xdelta3_execute, METH_VARARGS, "xdelta3 encode or decode"},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

static struct PyModuleDef xdelta3_module = {
   PyModuleDef_HEAD_INIT,
   "xdelta3",   /* name of module */
   "xdelta3", /* module documentation, may be NULL */
   0,     /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
   xdelta3_methods
};

PyMODINIT_FUNC PyInit__xdelta3(void) {
  return PyModule_Create(&xdelta3_module);
}
