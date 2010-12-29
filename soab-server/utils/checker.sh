#!/bin/sh

# This is used to run pyflakes against the source directory

ROOT_DIR=`pwd`/..
SRC_DIR=$ROOT_DIR/src

source $ROOT_DIR/setup_paths.sh
cd $SRC_DIR
pyflakes *.py
