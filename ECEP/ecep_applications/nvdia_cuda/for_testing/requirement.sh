#!/bin/bash

echo "cuda  for exe file"
nvcc /home/for_testing/vectoradd.cu
mv a.out /home
./home/a.out > /home/for_testing/output.log