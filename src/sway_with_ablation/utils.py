import math
import random
import config

from value import VALUE

def cosine(a, b, c):
  # print(f"a: {a}, b: {b}, c: {c}")
  if c == 0:
    return a or b

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


def o(t, isKeys=False):

  if not isinstance(t, dict):
    return str(t)

  sort_t_keys = list(t.keys())
  sort_t_keys.sort()
  sort_t = {f"{k} {t[k]}" for k in sort_t_keys}

  return "{:" + " :".join(sort_t) + "}"

def show(node, what, cols, nPlaces, lvl=0, global_stat=None):
  if node:

    # print('| '*lvl + str(len(node['data'].rows)) + '', end='')
    
    if ((not 'left' in node) or lvl==0):
      # print(o(node['data'].stats("mid", node['data'].cols.y, nPlaces)))
      if not 'left' in node:
        global_stat.addStat(node['data'].stats("mid", node['data'].cols.y, nPlaces))

    # else:
    #   print('')
    # print(o(node['data'].stats("mid", node['data'].cols.y, nPlaces)) if ((not 'left' in node) or lvl==0) else "")
    # show(node['left'], what, cols, nPlaces, lvl+1)
    show(node.get('left'), what, cols, nPlaces, lvl+1, global_stat)
    # show(node['right'], what, cols, nPlaces, lvl+1)
    show(node.get('right'), what, cols, nPlaces, lvl+1, global_stat)