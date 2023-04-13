from data import DATA
import utils

import os
dir_path = os.path.abspath(os.path.dirname(__file__))


data_file_list = []
for file in os.listdir(dir_path+'/../../data'):
  if file.endswith('.csv'):
    data_file_list.append(file)
data_file_list.sort()
print(data_file_list)

data_dir = '../../data/'

for file in data_file_list:
  # if file.startswith('S'):
  #   continue
  print(dir_path+'/'+data_dir+file)
  # read data
  # make data into DATA
  data = DATA(data_dir+file)
  # run on sway
  utils.show(data.sway(), "mid", data.cols.y, 1)

  print()
  

## continue on dist function




