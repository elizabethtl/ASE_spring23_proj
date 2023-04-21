from num import Num
from sym import Sym
from data import Data
from utils import *
# from numUtils import *
from config import *

##################
### test functions
def test_the():
  oo(the, 'test')

def test_copy():
  t1 =  {'a':1, 'b': {'c':2, 'd':3}}
  t2 = myCopy(t1)
  t2['b']['d'] = 10000
  print(f"b4 {t1}\nafter {t2}")

def test_sym():
  sym = Sym()
  for x in ['a', 'a', 'a', 'a', 'b', 'b', 'c']:
    sym.add(x)
  return 'a'==sym.mid() and 1.379==rnd(sym.div())

def test_num():
  num = Num()
  for x in [1, 1, 1, 1, 2, 2, 3]:
    num.add(x)
  return 11/7==num.mid() and 0.787==rnd(num.div())

def test_repcols():
  # t = repCols(exec(the['file']).cols)
  exec(open(the['file']).read())
  t = repCols(repgrid_value['cols'])
  # list(map(oo, t.cols.all))
  # map(oo, t.rows)
  for c in t.cols.all:
    oo(c)
  for r in t.rows:
    oo(r)

def test_synonyms():
  exec(open(the['file']).read())
  t = repCols(repgrid_value['cols'])
  # show(t.cluster())
  show(t.cluster(),"mid",t.cols.all,1)
  # show(repCols(exec(the['file']).cols).cluster())

def test_reprows():
  exec(open(the['file']).read())
  # t = repCols(repgrid_value['cols'])
  # t = exec(the['file'])
  rows = repRows(repgrid_value, transpose(repgrid_value['cols']))
  list(map(oo, rows.cols.all))
  list(map(oo, rows.rows))

def test_prototypes():
  exec(open(the['file']).read())
  # t = repCols(repgrid_value['cols'])
  rows = repRows(repgrid_value, transpose(repgrid_value['cols']))
  show(rows.cluster(), "mid", rows.cols.all, 1)

def test_position():
  exec(open(the['file']).read())
  rows = repRows(repgrid_value, transpose(repgrid_value['cols']))
  rows.cluster()
  repPlace(rows)

def test_every():
  repgrid(the['file'])