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
  print(dir_path+'/'+data_dir+file)

  data = DATA(data_dir+file)

  best, rest, evals = data.sway()
  rule, most = data.xpln(best, rest)
  print("-----------\nexplain=", utils.o(utils.showRule(rule)))

  sel = utils.selects(rule, data.rows)
  selected = [s for s in sel if s is not None]

  data1 = data.clone(selected)
  print("all                ", utils.o(data.stats()), utils.o(data.stats("div")))
  print("sway with", evals, "evals", utils.o(best.stats()), utils.o(best.stats("div")))
  print("xpln on",  evals, "evals  ", utils.o(data1.stats()), utils.o(data1.stats("div")))
  top, _ = data.betters(len(best.rows))
  top = data.clone(top)
  print("sort with", len(data.rows), "evals", utils.o(top.stats()), utils.o(top.stats("div")))


  print()