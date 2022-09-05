#!/bin/bash
export PATH=/mnt/d/keyan/abcbin:$PATH
export LD_LIBRARY_PATH=/mnt/d/keyan/dd/cudd-3.0.0/cudd:$LD_LIBRARY_PATH

sudo ln -s  /mnt/d/keyan/dd/cudd-3.0.0/cudd/.libs/libcudd-3.0.0.so.0   /usr/lib
sudo ldconfig