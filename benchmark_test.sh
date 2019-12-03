#!/bin/bash

time (
    (python3 example2.py &) ;
    (python3 distmm.py -v -n 2) ;
    (python3 distmm.py -v -n 2) ;
    (python3 distmm.py -v -n 2)
)