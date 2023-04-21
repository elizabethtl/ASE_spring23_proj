class ROW:
  def __init__(self, t):
    # self.cells = t
    import re
    tmp = [float(i) if re.search('[0-9]', i) else i for i in t]    
    # self.cells = t
    self.cells = tmp