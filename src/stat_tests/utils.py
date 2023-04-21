import config
import random

def NUM(t=None):
  i = {
    'n': 0,
    'mu': 0,
    'm2': 0,
    'sd': 0
  }
  if t==None:
    return i
  for x in t:
    add(i, x)
  return i

def add(i, x):
  i['n'] += 1
  d = x - i['mu']
  i['mu'] = i['mu'] + d/i['n']
  i['m2'] = i['m2'] + d*(x-i['mu'])
  i['sd'] = 0 if i['n']<2 else (i['m2']/(i['n']-1))**0.5


def samples(t, n=None):
  u = []
  length = n or len(t)-1
  for i in range(0, length):
    u.append(t[random.randint(0, len(t)-1)])
  return u


def delta(i, other):
  e = 10**-32
  y = i
  z = other
  # print(abs(y['mu'] - z['mu']))
  # print((e + (y['sd']**2)/y['n'] + (z['sd']**2)/z['n']))
  return abs(y['mu'] - z['mu']) / ((e + (y['sd']**2)/y['n'] + (z['sd']**2)/z['n'])**0.5)

def cliffsDelta(ns1, ns2):
  n, gt, lt = 0, 0, 0
  if len(ns1) > 128:
    ns1 = samples(ns1, 128)
  if len(ns2) > 128:
    ns2 = samples(ns2, 128)
  for x in ns1:
    for y in ns2:
      n += 1
      if x > y:
        gt += 1
      if x < y:
        lt += 1
  return abs(lt - gt)/n <= config._cliff

def bootstrap(y0, z0):
  x, y, z = NUM(), NUM(), NUM()
  yhat, zhat = [], []
  for y1 in y0:
    add(x, y1)
    add(y, y1)
  for z1 in z0:
    add(x, z1)
    add(z, z1)

  for y1 in y0:
    yhat.append(y1 - y['mu'] + x['mu'])
  for z1 in z0:
    zhat.append(z1 - z['mu'] + x['mu'])
  
  tobs = delta(y, z)
  n = 0
  for _ in range(0, config._bootstrap):
    if (delta(NUM(samples(yhat)), NUM(samples(zhat)))) > tobs:
      n += 1
  
  return n/config._bootstrap >= config._conf