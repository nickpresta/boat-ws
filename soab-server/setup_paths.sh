#!/bin/sh
# This sets up the paths needed for our project

export PYTHONPATH="`pwd`:`pwd`/site-packages:$PYTHONPATH"
export PATH="$PATH:`pwd`/site-packages/bin"
