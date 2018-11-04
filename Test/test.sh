#!/bin/bash

python ../py2latexpc.py test.py  1>test.txt  & latexmk test.tex -pdf
