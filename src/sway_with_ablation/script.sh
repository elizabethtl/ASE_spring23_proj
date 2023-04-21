#!/bin/sh

ls ../../data/auto2_ablation | while read i;
do
  echo ${i}
  python3 main.py ${i} > ../../etc/sway_with_ablation/${i}.out
done
