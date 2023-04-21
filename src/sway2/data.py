import csv
import math
import copy
import os
dir_path = os.path.abspath(os.path.dirname(__file__))
from operator import itemgetter
import random

from cols import COLS
from row import ROW
import config
import utils

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

  def stats(self, what, cols, nPlaces):
    c = cols or self.cols.y
    stat = {}
    for item in c:
      stat[item.txt] = item.rnd(getattr(item, what)(), nPlaces)
    return stat

  # return best half recursively
  def sway(self, rows=None, min=None, cols=None, above=None):
    rows = rows or self.rows
    min = min or (len(rows)**config._min)
    cols = cols or self.cols.x
    # node = {'data': self.clone(rows)}
    ### clone
    data = DATA(self.cols.names, 'col')
    for r in rows:
      data.addrow(r)
    node = {'data': data}

    if len(rows) >= 2*min:
      left, right, node['A'], node['B'], node['mid'], _ = self.half(rows, cols, above)
      if self.better(node['B'], node['A']):

      ## instead of comparing A, B, which is not actually in the two halves
      ## compare a random row from the two halves
      # mylen = len(left) if len(left) < len(right) else len(right)
      # rand_num = random.randint(0, mylen-1)
      # if self.better(left[rand_num], right[rand_num]):
        left, right, node['A'], node['B'] = right, left, node['B'], node['A']
      # node['left'] = self.sway(left, min, cols, node['A'])

      ## i removed node['a'] to increase randomness
      node['left'] = self.sway(left, min, cols)
    return node
  

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
    around = self.around(A, some)
    B = around[int((config._far*new_len)//1)]['row']
    c = dist(A, B)
    # the case where A, B have 
    # if c == 0:
    #   B = around[int((config._far*new_len)//1)]['row']

    left = []
    right = []

    def project(row):
      return {'row': row, 'dist': utils.cosine(dist(row, A), dist(row, B), c)}

    # sort based on distance to a row, then split into two
    for n, tmp in enumerate(sorted(map(project, rows), key=itemgetter('dist'))):

      # randomly swap appending to left and right

      if n <= len(rows)//2:
        # if random.randint(0, 1) > config._rand_swap:
        #   right.append(tmp['row'])
        #   continue
        left.append(tmp['row'])
        mid = tmp['row']
      else:
        # if random.randint(0, 1) > config._rand_swap:
        #   left.append(tmp['row'])
        #   continue
        right.append(tmp['row'])
    
    return left, right, A, B, mid, c
  
  # sort by distance to row1
  def around(self, row1, rows=None, cols=None):
    def func(row2):
      return {'row':row2, 'dist':self.dist(row1, row2, cols)}
    ret = sorted(list(map(func, rows or self.rows)), key=itemgetter('dist'), reverse=False)
    return ret
  
  def dist(self, row1, row2, cols=None):
    n = 0
    d = 0 

    # why comparing distance with cols.x (columns without +/-)
    # because cluster according to cols.x distance
    # getting y values is expensive
    for _, col in enumerate(cols if cols else self.cols.x):
      n += 1
      d += col.dist(row1.cells[col.at], row2.cells[col.at])**config._p

    ## add randomness to comparing cols.x
    d = d * (1+random.uniform(-config._randomness, config._randomness))

    # print(f"return: {(d/n)**(1/the['p'])}")
    return ((d/n)**(1/config._p)) 
  # * random.randint(-1, 1)*config._rand_dist


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
