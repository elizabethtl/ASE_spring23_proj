#!/bin/sh

ls ../../data | while read i;
do
  echo ${i}
  python3 main.py ${i} > ../../etc/sway1/${i}.out
done
