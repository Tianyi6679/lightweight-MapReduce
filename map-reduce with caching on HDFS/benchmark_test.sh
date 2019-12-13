#!/bin/bash

time (
    (python example2.py &) ;
    (python distmm.py -v -n 2) ;
    (python distmm.py -v -n 2) ;
    (python distmm.py -v -n 2)
)
