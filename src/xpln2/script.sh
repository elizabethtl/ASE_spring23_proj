#!/bin/sh

ls ../../data | while read i;
do
  echo ${i}
  python3 main.py ${i} > ../../etc/xpln2/${i}.out
done
