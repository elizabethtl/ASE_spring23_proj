from range import RANGE
import re
import config
import copy
import math

# SYM's get mapped to themselves but 
# NUM's get mapped to one of the.bins values

def bin(col, x):
  if "SYM" in str(type(col)):
    return x
  tmp = (col.hi - col.lo) / (config._bins - 1)
  if col.hi == col.lo:
    return 1
  else:
    return math.floor(x/tmp + 0.5)*tmp

def bins(cols, rowss):
  out = []
  for col in cols:
    ranges = {}
    for y, rows in rowss.items():
      for row in rows:
        # x, k = row[col['at']]
        x = row.cells[col.at]
        # print(type(x))
        # x = int(float(x)) if re.search('[0-9]', x) else x
        if x != '?':
          k = bin(col, x)
          # print(k)
          # print(type(k))
          # print(re.search('[0-9]', k))
          char_k = k
          # char_k = int(float(k)) if re.search('[0-9]', k) else k
          if char_k not in ranges:
            ranges[char_k] = RANGE(col.at, col.txt, x)
          ranges[char_k].extend(x, y)
    def itself(x):
      return x
    ranges = list(dict(sorted(ranges.items())).values())
    
    if 'SYM' in str(type(col)):
    # if 'isSym' in col and col['isSym']:
      out.append(ranges)
    else:
      out.append(mergeAny(ranges))
  return out

def mergeAny(ranges0):
  def noGaps(t):
    for j in range(1, len(t)):
      t[j].lo = t[j-1].hi
    t[0].lo = -math.inf
    t[len(t)-1].hi = math.inf
    return t
  ranges1 = []
  j = 0
  while j < len(ranges0):
    left = ranges0[j]
    right = None if j == len(ranges0)-1 else ranges0[j+1]
    if right:
      y = merge2(left.y, right.y)
      if y:
        j += 1
        left.hi = right.hi
        left.y = y
    ranges1.append(left)
    j += 1
  if len(ranges0) == len(ranges1):
    return noGaps(ranges0)
  else:
    return mergeAny(ranges1)
  
def merge2(col1, col2):
  new = merge(col1, col2)
  # print(new.div(), new.n)
  # print(col1.div(), col1.n)
  # print(col2.div(), col2.n)
  if new.div() <= (col1.div()*col1.n + col2.div()*col2.n)/new.n:
    return new

def merge(col1, col2):
  new = copy.deepcopy(col1)
  if "SYM" in str(type(col1)):
  # if col1['isSym']:
    for x, n in col2.has.items():
      new.add(x, n)
  else:
    for n in col2.has:
      new.add(n)
      new.lo = min(col1.lo, col2.lo)
      new.hi = max(col1.hi, col2.hi)
  return new