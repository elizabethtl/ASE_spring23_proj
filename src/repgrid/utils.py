
import re
import sys
import os
import copy
dir_path = os.path.abspath(os.path.dirname(__file__))

import math

from config import *
# from numUtils import *
# from listUtils import *
from data import Data

###########
### strings
def o(t, isKeys=False):

  if not isinstance(t, dict):
    return str(t)

  sort_t_keys = list(t.keys())
  sort_t_keys.sort()
  sort_t = {f"{k} {t[k]}" for k in sort_t_keys}

  ###
  print(t.__dict__)
  return t.__dict__
  # return "{:" + " :".join(sort_t) + "}"

def oo(t, test=None):
  if test=='test':
    print(t)
    return
  if(isinstance(t, list)):
    print(t)
    return
  # if(isinstance(t, dict)):
    
  if t.__dict__:
    t = t.__dict__
    # print(type(t), type(t).__name__)
    # if(__name__ in t):
    #   print(t.__module__)
    # if()
    # t['a'] = t.__module__
    # t['a'] = t.__class__.__name__
    # if('Num' in str(type(t))):
    #   t['a'] = 'Num'
    # elif('Sym' in str(type(t))):
    #   t['a'] = 'Sym'
    # elif('Row' in str(type(t))):
    #   t['a'] = 'Row'
  t['id'] = id(t)
  t = dict(sorted(t.items()))
  print(t)
  # print(o(t))
  return t

def eg(key, str, fun):
  egs[key] = fun
  global help
  help = help + "  -g  "+key+"\t"+str+"\n"

#######
### csv
def csv(filename, csv_fun):

  ######
  # print(f"csv filename {filename}")
  # print(f"fun_csv {fun_csv}")

  s = open(dir_path+'/'+filename, 'r')
  lines = s.readlines()
  t = []
  for line in lines:
    # t = []
    row = []
    for s1 in line.split(','):
      s1 = s1.replace('\n', '')
      row.append(coerce(s1))
    t.append(row)
    
    #######
    # print(f"csv t")
    # print(t)
    # t = ['Clndrs', 'Volume', 'Hp:', 'Lbs-', 'Acc+', 'Model', 'origin', 'Mpg+']
    # t = [8.0, 304.0, 193.0, 4732.0, 18.5, 70.0, 1.0, 10.0]
    # ....

    csv_fun(row)
  
#######
### cli
def cli(options):
  for k, v in options.items():
    v = str(v)

    argv = sys.argv[1:]
    for n, x in enumerate(argv):
      if x=='-'+k[0] or x=='--'+k:
        if v == 'false':
          v = 'true'
        if v == 'true':
          v = 'false'
        else:
          v = argv[n+1]
      options[k] = coerce(v)

  # print(options)
  return options

############
### settings
def settings(s):
  t = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
  return dict(t)

##########
### coerce
def coerce(s):
  if s == "true": return True
  elif s == "false": return False
  else:
    try:
      return float(s)
    except:
        return s

## print the tree
def show(node, what, cols, nPlaces, lvl=0):
  if node:

    print('|..'*lvl, end='')
    
    if ((not 'left' in node)):
      print(o(last(last(node['data'].rows).cells)))
    else:
      print(int(rnd(100*node['c'], 0)))
    # print(o(node['data'].stats("mid", node['data'].cols.y, nPlaces)) if ((not 'left' in node) or lvl==0) else "")
    # show(node['left'], what, cols, nPlaces, lvl+1)
    show(node.get('left'), what, cols, nPlaces, lvl+1)
    # show(node['right'], what, cols, nPlaces, lvl+1)
    show(node.get('right'), what, cols, nPlaces, lvl+1)


#######
### rep
def repCols(cols):
  cols = myCopy(cols)
  # print(type(cols))
  # cols is a list of lists
  for _,col in enumerate(cols):
    # print(col)
    col[len(col)-1] = col[0]+":"+col[len(col)-1]
    for j in range (1, len(col)):
      col[j-1] = col[j]
    col.pop()

  # def func(k, v):
  #   return "Num"+str(k)
  insert_col = ["Num"+str(k+1) for k in range(len(cols[0]))]
  cols.insert(0, insert_col)

  # cols.insert(0, map(lambda x: "Num"+str(x), cols[0]))
  # cols.insert(0, myMap(cols[0], func))
  cols[0][len(cols[0])-1] = "thingX"
  return Data(cols)
  
def repRows(t, rows, u=None):
  rows = myCopy(rows)
  for j, s in enumerate(rows[len(rows)-1]):
    rows[0][j] = rows[0][j]+":"+s
  rows.pop()
  for n, row in enumerate(rows):
    if n == 0:
      row.append("thingX")
    else:
      u = t['rows'][len(t['rows'])-1 - n + 1]
      row.append(u[len(u)-1])
  return Data(rows)

def transpose(t, n = None):
  u = []
  for i in range(len(t[0])):
    u.append([])
    for j in range(len(t)):
      u[i].append(t[j][i])
  return u

def repPlace(data):
  n, g = 20, []
  for i in range(n+1):
    g.append([])
    for j in range(n+1):
      g[i].append(" ")
  maxy = 0
  print()
  for r, row in enumerate(data.rows):
    c = chr(97+r).upper()
    print(c, last(row.cells))
    x, y = int(row.x*n//1), int(row.y*n//1)
    maxy = max(maxy, y+1)
    g[y+1][x+1] = c
  print()
  for y in range(maxy):
    oo(g[y])

def repgrid(sFile):
  exec(open(the['file']).read())
  cols = repCols(repgrid_value['cols'])
  rows = repRows(repgrid_value, transpose(repgrid_value['cols']))
  show(rows.cluster(), "mid", rows.cols.all, 1)
  show(cols.cluster(), "mid", cols.cols.all, 1)
  repPlace(rows)

#######
### num

def rand(lo, hi):
  lo = lo or 0
  hi = hi or 1
  global Seed 
  Seed = (16807 * Seed) % 2147483647
  return lo + (hi-lo) * Seed / 2147483647


def my_rint(lo, hi):
  ######
  # print('rint')
  return math.floor(0.5 + rand(lo, hi))

def rnd(n, nPlaces=3):
  # print(f"rnd n:{n}")
  nP = nPlaces
  mult = 10**nP
  return math.floor(n*mult + 0.5)/mult

def cosine(a, b, c):
  # print(f"a: {a}, b: {b}, c: {c}")

  #######
  ## sometime c=0
  # if(c == 0):
  #   return 0, 0

  x1 = (a**2 + c**2 - b**2) / (2*c)
  x2 = max(0, min(1, x1))
  y = abs((a**2 - x2**2)) ** 0.5

  if isinstance(y, complex):
    print(f"a = {a}, b = {b}, c = {c}")
    print(f"x1 = {x1}, x2 = {x2}, y = {y}")
  return x2, y

def myCopy(t, u=None):
  return copy.deepcopy(t)

  # list or dict ??
  # if isinstance(t, list):
  #   return t
  # def func(k, v):
  #   return copy(v), copy(k)

  # u = kap(t, func)
  # # setmetatable(u, getmetatable(t))
  # return {u, t}
  


########
### list

def myMap(t, fun):
  # print(f"map(), len of t: {len(t)}")
  u = {}
  for k, v in enumerate(t):
    # print(f"map(), k: {k}, v:{v}")
    # v, k = fun(v)
    v = fun(v)
    # print(f"fun(), v: {v}, k:{k}")
    # i = k if k else (1+len(u))
    # i = k if k else (len(u))
    i = k
    u[i] = v
  # print(f"map(), u: {u}")
  return u

def kap(t, fun):
  # print(f"kap(), t: {t}")
  u = {}
  for k, v in enumerate(t):
    # print(f"kap(), k: {k}, v:{v}")
    v, k = fun(k, v)
    # print(f"fun(), v: {v}, k:{k}")
    # i = k or (1+len(u))
    i = k if k else (len(u))
    u[i] = v
  
  return u

def sort(t, fun):
  print("t in sort()")
  # print(t)
  print("key in sort()")
  print(fun, type(fun))
  # t.sort(key=fun)
  # return t
  return sorted(t, key=fun)

def any(t):
  return t[my_rint(0, len(t)-1)]

def many(t, n):
  # print(f"n: {n}")
  u = []
  for i in range(int(n)):
    u.append(any(t))
  return u

def last(t):
  return t[len(t)-1]