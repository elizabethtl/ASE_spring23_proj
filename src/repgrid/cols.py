import re

from num import Num
from sym import Sym

class Cols:
  def __init__(self, t):
    self.names = t
    self.all = []
    self.x = []
    self.y = []
    self.klass = {}

    for n, s in enumerate(t):
      ######
      # print(f"cols n:{n}, s:{s}")
      # print(re.search("^[A-Z]+", s))
      col = Num(n, s) if re.search("^[A-Z]+", s) else Sym(n, s)
      self.all.append(col)
      if not re.search("X$", s):
        if re.search("!$", s):
          self.klass = col
        self.y.append(col) if re.search("[!+-]$", s) else self.x.append(col)



  def add(self, row):
    for _,t in enumerate([self.x, self.y]):
      for _,col in enumerate(t):
        col.add(row.cells[col.at])