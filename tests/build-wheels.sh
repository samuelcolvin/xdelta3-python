#!/bin/bash
set -e -x

yum install -y gcc
gcc -v

# Compile wheels
/opt/python/cp36-cp36m/bin/pip install -r /io/tests/requirements.txt
/opt/python/cp36-cp36m/bin/pip wheel /io/ -w wheelhouse/

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done
