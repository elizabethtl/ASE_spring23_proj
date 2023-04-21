import math
import re

# from numUtils import *
from utils import *

class Num:
  def __init__(self, at=0, txt=''):
    # print(f"txt:{txt}")
    
    self.at = at
    self.txt = txt
    self.n = 0
    self.mu = 0
    self.m2 = 0
    self.lo = math.inf
    self.hi = -math.inf
    # print(re.search("-$", self.txt))
    self.w = -1 if re.search("-$", self.txt) else 1

  def add(self, x):
    if x != "?":
      self.n = self.n + 1
      d = x - self.mu
      self.mu = self.mu + d/self.n
      self.m2 = self.m2 + d*(x - self.mu)
      self.lo = min(x, self.lo)
      self.hi = max(x, self.hi)
  
  def mid(self):
    return self.mu

  # return standard deviation
  def div(self):
    return 0 if (self.m2<0 or self.n<2) else math.pow((self.m2/(self.n-1)), 0.5)

  def rnd(self, x, n):
    return x if x=="?" else rnd(x, n)

  def norm(self, n):
    return n if n== "?" else (n-self.lo)/(self.hi-self.lo+1e-32)

  def dist(self, n1, n2):
    if n1=="?" and n2=="?":
      return 1
    n1 = self.norm(n1)
    n2 = self.norm(n2)
    if n1=="?":
      n1 = 1 if n2<0.5 else 0
    if n2=="?":
      n2 = 1 if n1<0.5 else 0  
    return abs(n1-n2)