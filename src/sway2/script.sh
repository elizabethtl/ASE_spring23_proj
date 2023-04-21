#!/bin/sh

ls ../../data | while read i;
do
  echo ${i}
  python3 main.py ${i} > ../../etc/sway2.2/${i}.out
done
