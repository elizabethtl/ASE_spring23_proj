from sym import SYM

class RANGE:
  
  def __init__(self, at, txt, lo, hi=None):
    self.at = at
    self.txt = txt
    self.lo = lo
    self.hi = hi or lo
    self.y = SYM()

  def extend(self, n, s):
    self.lo = min(n, self.lo)
    self.hi = max(n, self.hi)
    self.y.add(s)
