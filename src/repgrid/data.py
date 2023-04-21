# from utils import *
# from numUtils import *
# from listUtils import *
from row import Row
from cols import Cols
from operator import itemgetter
import math
from config import the

class Data:
  def __init__(self, src={}, c=None):

    #######
    # print(f"data src: {src}")

    self.rows = []
    # self.rows = {}
    self.cols = None

    # fun = lambda x: self.add(x)

    if(c == 'col'):
      self.add(src)
    elif isinstance(src, str):
      # csv(src, lambda x: self.add(x))
      from utils import csv
      csv(src, self.add)
    else:
      # map(lambda x: self.add(x), src)
      # map(self.add, src)
      for row in src:
        # print(row)
        self.add(row)

    ######
    # print(f"data.cols {self.cols}")
  
  def add(self, t):
    ######
    # print(f"data.add t:{t}")
    if self.cols:
      # make t a Row
      t = t if "Row" in str(type(t)) else Row(t)
      # t = t if  else Row(t)
      self.rows.append(t)
      # self.rows.update(t)
      self.cols.add(t)
    else:
      self.cols = Cols(t)

  def clone(self, init={}):
    ######
    # print(f"clone self.cols.names: {self.cols.names}")
    # print(f"clone init len: {len(init)}")
    
    data = Data(self.cols.names, 'col')
    # data = Data([self.cols.names])

    from utils import myMap
    myMap(init,lambda x: data.add(x))
    return data

  # def stats(self, what, cols, nPlaces):
  #   def fun(k, col):
  #     return col.rnd(getattr(col, what)(), nPlaces), col.txt
    
  #   return kap(cols or self.cols.y, fun)

  def dist(self, row1, row2, cols=None):
    n = 0
    d = 0 

    ######
    # print("data.dist")
    # print(cols)
    # print(cols if cols else self.cols.x)

    for _, col in enumerate(cols if cols else self.cols.x):

      # print("data.dist col")
      # print(col.at)
      # print(f"row1.cells[col.at]: {row1.cells[col.at]}")
      # print(f"row2.cells[col.at]: {row2.cells[col.at]}")

      n += 1
      # ^ operator is XOR in python
      d += col.dist(row1.cells[col.at], row2.cells[col.at])**the['p']
    # print(f"return: {(d/n)**(1/the['p'])}")
    return (d/n)**(1/the['p'])
  
  def around(self, row1, rows=None, cols=None):
    def func(row2):
      ######
      # print("data.around")
      # print("row1.cells")
      # print(row1.cells)
      # print("row2.cells")
      # print(row2.cells)
      return {'row':row2, 'dist':self.dist(row1, row2, cols)}
    return sorted(list(map(func, rows or self.rows)), key=itemgetter('dist'))

  def half(self, rows=None, cols=None, above=None):

    # rows = rows if rows else self.rows
    rows = rows or self.rows
    # some = many(rows, the['Sample'])

    def dist(row1, row2):
      return self.dist(row1, row2, cols)

    from utils import any
    A = above if above else any(rows)
    B = self.furthest(A, rows)['row']
    c = dist(A, B)
    left = []
    right = []

    def project(row):
      from utils import cosine
      x, y = cosine(dist(row, A), dist(row, B), c)
      # row.x = row.x if row.x else x
      # row.y = row.y if row.y else y
      try:
        row.x = row.x
        row.y = row.y
      except:
        row.x = x
        row.y = y
      return {'row': row, 'x': x, 'y': y}

    for n, tmp in enumerate(sorted((map(project, rows)), key=itemgetter('x'))):
      ###
      # print(n, len(rows)//2)
      if n < len(rows)//2:
        left.append(tmp['row'])
        mid = tmp['row']
      else:
        right.append(tmp['row'])
    
    return left, right, A, B, mid, c

  def cluster(self, rows=None, min=None, cols=None, above=None):

    rows = rows or self.rows
    cols = cols or self.cols.x
    node = {'data':self.clone(rows)}
    ######
    # print('node')
    # print(node)

    if len(rows) >= 2:
      left, right, node['A'], node['B'], node['mid'], node['c'] = self.half(rows, cols, above)
      node['left'] = self.cluster(left, min, cols, node['A'])
      node['right'] = self.cluster(right, min, cols, node['B'])
    
    return node

  def better(self, row1, row2):
    s1 = 0
    s2 = 0
    ys = self.cols.y
    for _, col in enumerate(ys):
      x = col.norm(row1.cells[col.at])
      y = col.norm(row2.cells[col.at])
      s1 = s1 - math.exp(col.w*(x-y)/len(ys))
      s2 = s2 - math.exp(col.w*(y-x)/len(ys))
    return s1/len(ys) < s2/len(ys)

  def sway(self, rows=None, min=None, cols=None, above=None):
    rows = rows or self.rows
    min = min or (len(rows)**the['min'])
    cols = cols or self.cols.x
    node = {'data': self.clone(rows)}

    if len(rows) >= 2*min:
      left, right, node['A'], node['B'], node['mid'], _ = self.half(rows, cols, above)
      if self.better(node['B'], node['A']):
        left, right, node['A'], node['B'] = right, left, node['B'], node['A']
      node['left'] = self.sway(left, min, cols, node['A'])
    return node

  def furthest(self, row1, rows=None, cols=None):
    t = self.around(row1, rows, cols)
    return t[len(t)-1]