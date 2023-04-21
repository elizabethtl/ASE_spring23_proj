import math
import random
import config
import re
from operator import itemgetter

def cosine(a, b, c):
  # print(f"a: {a}, b: {b}, c: {c}")
  if c == 0:
    return 0, 0

  x1 = (a**2 + c**2 - b**2) / (2*c)
  x2 = max(0, min(1, x1))
  y = abs((a**2 - x2**2)) ** 0.5

  if isinstance(y, complex):
    print(f"a = {a}, b = {b}, c = {c}")
    print(f"x1 = {x1}, x2 = {x2}, y = {y}")
  return x2, y

def rnd(n, nPlaces=3):
  # print(f"rnd n:{n}")
  return math.floor(n*(10**nPlaces) + 0.5)/(10**nPlaces)

def any(t):
  ## the following line makes any() always return the same row
  # random.seed(config._seed)
  return t[random.randint(0, len(t)-1)]

def many(t, n):
  # print(f"n: {n}")
  u = []
  for i in range(int(n)):
    u.append(any(t))
  return u


def o(t, stat=None):

  if not isinstance(t, dict):
    return str(t)

  sort_t_keys = list(t.keys())
  sort_t_keys.sort()
  sort_t = {f"{k} {t[k]}" for k in sort_t_keys}

  if stat:
    stat.addStat(t)

  return "{:" + " :".join(sort_t) + "}"

def show(node, what, cols, nPlaces, lvl=0):
  if node:

    print('| '*lvl + str(len(node['data'].rows)) + '', end='')
    
    if ((not 'left' in node) or lvl==0):
      print(o(node['data'].stats("mid", node['data'].cols.y, nPlaces)))
    else:
      print('')
    # print(o(node['data'].stats("mid", node['data'].cols.y, nPlaces)) if ((not 'left' in node) or lvl==0) else "")
    # show(node['left'], what, cols, nPlaces, lvl+1)
    show(node.get('left'), what, cols, nPlaces, lvl+1)
    # show(node['right'], what, cols, nPlaces, lvl+1)
    show(node.get('right'), what, cols, nPlaces, lvl+1)

### prune rules
# tho doesn't seem like its actually pruning
def prune(rule, maxSize):
  # print('prune')
  # print(rule)
  n = 0
  for txt, ranges in rule.items():
    n += 1
    if len(ranges) == maxSize[txt]:
      n += 1
      rule[txt] = None
  if n > 0:
    # print('return')
    # print(rule)
    return rule
  
### sort these ranges by how well they select for best using probability * support = b^2/(b+r)
def value(has, nb=1, nr=1, sGoal=True):
  b = 0
  r = 0
  for x, n in has.items():
    if x == sGoal:
      b += n
    else:
      r += n
  b = b / (nb + 1/math.inf)
  r = r / (nr + 1/math.inf)
  return b**2/(b+r)

def firstN(sortedRanges, scoreFun):
  # print()

  def func(r):
    print(r['range'].txt, r['range'].lo, r['range'].hi, rnd(r['val']), o(r['range'].y.has))
  # list(map(func, sortedRanges))
  first = sortedRanges[0]['val']
  def useful(range):
    if(range['val'] > 0.05 and range['val'] > first/10):
      return range
  # sortedRanges = map(useful, sortedRanges)
  sortedRanges = [x for x in sortedRanges if useful(x)]
  most, out = -1, -1
  # not sure if python slice is the same as the slice() in the lua code
  for n in range(1, len(sortedRanges)+1):
    split = sortedRanges[0:n]
    split_range = [x['range'] for x in split]
    tmp, rule = scoreFun(split_range)
    if tmp and tmp > most:
      out, most = rule, tmp
  return out, most

def showRule(rule):
  def pretty(range):
    # return range['lo'] if range['lo']==range['hi'] else [range['lo'], range['hi']]
    l = range.lo
    h = range.hi
    li = [range.lo, range.hi]
    return range.lo if range.lo==range.hi else [range.lo, range.hi]
  def merge(t0):
    # t is new list of ranges merged from t0?
    t, j = [], 1
    while j <= len(t0):
      left = t0[j-1]
      if j < len(t0):
        right = t0[j]
      else:
        right = None
      if right and left.hi == right.lo:
        left.hi = right.hi
        j += 1
      # t.append({'lo':left.lo, 'hi':left.hi})
      from rule import RULE
      t.append(RULE(left.lo, left.hi))
      j += 1
    return t if len(t0) == len(t) else merge(t)
  def merges(ranges):
    # return list(map(pretty, merge(sorted(ranges, key=itemgetter('lo'))))), attr
    return list(map(pretty, merge(sorted(ranges, key=lambda x: x.lo))))

  # return my_map(rule, merges)   

  u = {}
  for attr, ranges in rule.items():
    ## exist 'None' ranges
    if ranges == None:
      continue
    u[attr] = merges(ranges)
  return u

def my_map(t, fun):
  u = {}
  for k, v in t.items():
    v, k = fun(k, v)
    i = k if k else (len(u))
    u[i] = v
  return u

def selects(rule, rows):

  # for one attribute with multiple ranges
  # if any range matches the row, we return true.
  def disjunction(ranges, row):
    if ranges == None:
      return False
    for range in ranges:
      lo, hi, at = range.lo, range.hi, range.at
      x = row.cells[at]
      # x = int(float(row.cells[at])) if re.search('[0-9]', row.cells[at]) else row.cells[at]
      if x == '?':
        return True
      if lo == hi and lo == x:
        return True
      if lo <= x and x < hi:
        return True
    return False
  
  # for one rule with multiple attributes
  # if any attribute does not match the row, we return false.
  def conjunction(row):
    for ranges in rule.values():

      if not disjunction(ranges, row):
        return False
    return True
  
  def func(r):
    if None in r.cells or r.cells is None:
      # print(f"func(r):")
      # print(r)  
      return
    if conjunction(r):
      return r
  
  return list(map(func, rows))
  # return [row for row in list(map(func, rows)) if row is not None]
  # return_list = []
  # for row in rows:
  #   return_list.