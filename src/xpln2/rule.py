import utils

class RULE:
  def __init__(self, lo, hi, at=None):
    self.lo = lo
    self.hi = hi
    self.at = at


def rule_list(ranges, maxSize):
  t = {}
  for range in ranges:
    if range.txt not in t:
      t[range.txt] = []
    (t[range.txt]).append(RULE(range.lo, range.hi, range.at))
    # (t[range.txt]).append({'lo': range.lo, 'hi': range.hi, 'at': range.at})
  return utils.prune(t, maxSize)



