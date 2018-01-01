#!/bin/bash
for i in `seq 20 60`; do
  K=$(echo "scale=2; $i/20" | bc)
  COEFICIENT=$K python tournament.py
done
