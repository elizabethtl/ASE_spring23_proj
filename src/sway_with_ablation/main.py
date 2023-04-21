from data import DATA
import utils
import sys
from value import VALUE
import config
import time
import random

import os
dir_path = os.path.abspath(os.path.dirname(__file__))


# data_file_list = []
# for file in os.listdir(dir_path+'/../../data'):
#   if file.endswith('.csv') and file.startswith('nasa'):
#     data_file_list.append(file)
# data_file_list.sort(reverse=True)
# print(data_file_list)
# print()

file = sys.argv[1]
# file = 'auto2.csv'

data_dir = '../../data/auto2_ablation/'

# for file in data_file_list:
  # if file.startswith('S'):
  #   continue
print(dir_path+'/'+data_dir+file)
print()

print(f"min: {config._min}")
print(f"far: {config._far}")


sample_size_list = [10, 25, 50, 100, 200, 500, 1000]
for size in sample_size_list:
  config._sample = size
  print()
  print(f"sample: {config._sample}")



  global_stat = VALUE(file)
  
  start = time.time()

  for i in range(20):
    random.seed(config._seed+i)
    # read data 
    # make data into DATA
    data = DATA(data_dir+file)
    # run on sway
    utils.show(data.sway(), "mid", data.cols.y, 1, 0, global_stat)

  end = time.time()
  print(f"execution time: {end-start} seconds")

print()
  

## continue on dist function




