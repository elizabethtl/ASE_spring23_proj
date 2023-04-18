import csv
import math
import random
import os
dir_path = os.path.abspath(os.path.dirname(__file__))
from operator import itemgetter

from cols import COLS
from row import ROW
import config
import utils
from rule import rule_list
import discretization

class DATA:
  def __init__(self, src={}, c=None):
    self.rows = []
    self.cols = None

    if(c == 'col'):
      self.addrow(src)
    
    else:
      with open(dir_path+'/'+src, newline='') as csvfile:
        file_data = csv.reader(csvfile, delimiter=',')
        for row in file_data:
          self.addrow(row)

  def addrow(self, t):
    # print(t)
    # check if made cols (header) yet
    if self.cols:
      # print('append', t)
      # make t a ROW
      t = t if "ROW" in str(type(t)) else ROW(t)
      self.rows.append(t)

      ## what is this for?
      self.cols.add(t)

    else:
      self.cols = COLS(t)

  def stats(self, what="mid", cols=None, nPlaces=2):
    c = cols or self.cols.y
    stat = {}
    for item in c:
      stat[item.txt] = item.rnd(getattr(item, what)(), nPlaces)
    return stat
    # def fun(k, col):
    #   return col.rnd(getattr(col, what)(), nPlaces), col.txt
    # return kap(cols or self.cols.y, fun)

  def clone(self, init={}):
    data = DATA(self.cols.names, 'col')
    for r in init:
      data.addrow(r)
    return data

  # return best, rest half recursively
  def sway(self, rows=None, min=None, cols=None, above=None):

    def worker(rows, worse, evals0=None, above=None):
      if len(rows) <= len(self.rows)**config._min:
        # get random item from 
        tmp = []
        for i in range(0, int(config._rest*len(rows))):
          tmp.append(random.choice(worse))
        return rows, tmp, evals0  
      else:
        l, r, A, B, c, evals = self.half(rows, None, above)
        if self.better(B, A):
          l, r, A, B = r, l, B, A
        for row in r:
          worse.append(row)
        return worker(l, worse, evals+evals0, A)

    best, rest, evals = worker(self.rows, [], 0)
    return self.clone(best), self.clone(rest), evals

  def half(self, rows=None, cols=None, above=None):
    rows = rows if rows else self.rows
    some = utils.many(rows, config._sample)  # generate sample number of rows

    def dist(row1, row2):
      return self.dist(row1, row2, cols)

    A = above if above else utils.any(some)
    # B = self.around(A, some)[int((config._far*len(rows))//1)]['row']
    # print(int((config._far*len(rows))//1))

    # sample size might be too large, larger than 512
    new_len = len(rows)
    if config._sample < len(rows):
      new_len = config._sample
    B = self.around(A, some)[int((config._far*new_len)//1)]['row']

    c = dist(A, B)
    left = []
    right = []

    def project(row):
      return {'row': row, 'dist': utils.cosine(dist(row, A), dist(row, B), c)}

    # sort based on distance to a row, then split into two
    for n, tmp in enumerate(sorted(map(project, rows), key=itemgetter('dist'))):
      if n <= len(rows)//2:
        left.append(tmp['row'])
        mid = tmp['row']
      else:
        right.append(tmp['row'])
    
    return left, right, A, B, mid, c
  
  # sort by distance to row1
  def around(self, row1, rows=None, cols=None):
    def func(row2):
      return {'row':row2, 'dist':self.dist(row1, row2, cols)}
    ret = sorted(list(map(func, rows or self.rows)), key=itemgetter('dist'))
    return ret
  
  def dist(self, row1, row2, cols=None):
    n = 0
    d = 0 
    for _, col in enumerate(cols if cols else self.cols.x):
      n += 1
      d += col.dist(row1.cells[col.at], row2.cells[col.at])**config._p
    # print(f"return: {(d/n)**(1/the['p'])}")
    return (d/n)**(1/config._p)

  def better(self, row1, row2):
    s1 = 0
    s2 = 0
    ys = self.cols.y
    for _, col in enumerate(ys):
      # print(col)
      x = col.norm(row1.cells[col.at])
      y = col.norm(row2.cells[col.at])
      # x = row1.cells[col.at]
      # y = row2.cells[col.at]
      s1 = s1 - math.exp(col.w*(x-y)/len(ys))
      s2 = s2 - math.exp(col.w*(y-x)/len(ys))
    return s1/len(ys) < s2/len(ys)

  def betters(self, n):
    # stuck on how to make sorted work
    tmp = sorted(self.rows, key=lambda row:self.better(row, self.rows[self.rows.index(row)-1]))
    # tmp = sorted(data['rows'], cmp=lambda x,y:better(data, x, y))
    return (tmp[0:n], tmp[n+1:]) if n else tmp
  

  def xpln(self, best, rest):
    def v(has):
      return utils.value(has, len(best.rows), len(rest.rows), "best")
    def score(ranges):
      rule = rule_list(ranges, maxSizes)
      if rule:
        # oo(showRule(rule))
        print(utils.showRule(rule))
        bestr = utils.selects(rule, best.rows)
        restr = utils.selects(rule, rest.rows)

        if len(bestr)+len(restr) > 0:
          return v({'best': len(bestr), 'rest': len(restr)}), rule
    tmp, maxSizes = [], {}

    print('range', 'range.lo', 'range.hi')
    for ranges in (discretization.bins(self.cols.x, {'best': best.rows, 'rest': rest.rows})):
      maxSizes[ranges[0].txt] = len(ranges)
      print()
      
      for range in ranges:
        print(range.txt, range.lo, range.hi)
        tmp.append({'range': range, 'max': len(ranges), 'val': v(range.y.has)})
    
    # reverser=True ??
    rule, most = utils.firstN(sorted(tmp, key=itemgetter('val')), score)
    return rule, most
  

