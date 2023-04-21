from data import DATA
import sys
import utils
import random
import config
from value import VALUE
import os
dir_path = os.path.abspath(os.path.dirname(__file__))

file = sys.argv[1]
# file = 'auto93.csv'

data_dir = '../../data/'

print(dir_path+'/'+data_dir+file)

data = DATA(data_dir+file)

sway_stat = VALUE(file, 'sway')
xpln_stat = VALUE(file, 'xpln')
top_stat = VALUE(file, 'top')

for i in range(20):
  random.seed(config._seed+i)

  best, rest, evals = data.sway()
  rule, most = data.xpln(best, rest)
  print("-----------\nexplain =", utils.o(utils.showRule(rule)))

  sel = utils.selects(rule, data.rows)
  selected = [s for s in sel if s is not None]

  data1 = data.clone(selected)
  print("all              ", utils.o(data.stats()), utils.o(data.stats("div")))
  print("sway with", evals, "evals", utils.o(best.stats(), sway_stat), utils.o(best.stats("div")))
  print("xpln on",  evals, "evals  ", utils.o(data1.stats(), xpln_stat), utils.o(data1.stats("div")))
  # top, _ = data.betters(len(best.rows))
  # top = data.clone(top)
  # print("sort with", len(data.rows), "evals", utils.o(top.stats(), top_stat), utils.o(top.stats("div")))


  print()