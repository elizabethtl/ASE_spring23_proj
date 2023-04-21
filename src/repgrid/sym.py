import math

class Sym:
  def __init__(self, at=0, txt=''):
    ######
    # print(f"sym {txt}")
    
    self.at = at 
    self.txt = txt
    self.n = 0
    self.has = {}
    self.most = 0
    self.mode = None
  
  def add(self, x):
    if x != "?":
      self.n += 1
      self.has[x] = 1 + (self.has[x] if x in self.has else 0)
      
      if self.has[x] > self.most:
        self.most = self.has[x]
        self.mode = x
  
  def mid(self):
    return self.mode
  
  # return entropy
  def div(self):
    def fun(p):
      return p*math.log(p, 2)
    
    e = 0
    for _, n in self.has.items():
      e = e + fun(n/self.n)
    
    return -e

  def rnd(self, x, n):
    return x

  def dist(self, s1, s2):
    return 1 if (s1=="?" and s2=="?") else (0 if (s1==s2) else 1) 
    