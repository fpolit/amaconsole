#!/bin/bash

CLEAN=1
CLEAN_PYCACHE=1
GFILES=(amaconsole.egg-info dist build amaconsole/__init__.py)  # generated files and directories
RUNTESTS=1
BUILD_DIR=build

if [[ $CLEAN -eq 1 ]]; then
    rm -rf ${GFILES[@]}
fi

if [[ $CLEAN_PYCACHE -eq 1 ]]; then
    rm -rf $(find amaconsole -name __pycache__ -type d)
fi

mkdir -p $BUILD_DIR
cmake -S . -B $BUILD_DIR -DCMAKE_BUILD_TYPE=Debug \
                        -DCMAKE_COMPILER_WALL=ON \
                        -DCMAKE_BUILD_TESTS=ON \
			-DGIT_UPDATE_SUBMODULES=ON \
                        --log-level=DEBUG || exit 1
make -C $BUILD_DIR

if [[ $? -eq 0 ]]; then
    sudo make -C $BUILD_DIR install
fi

if [[ $? -eq 0 && $RUNTESTS -eq 1 ]]; then
    make -C $BUILD_DIR pytest
    make -C $BUILD_DIR test # C/CXX tests
fi
