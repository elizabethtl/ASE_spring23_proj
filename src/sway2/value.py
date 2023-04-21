

class VALUE:
  def __init__(self, dataset):
    self.dataset = dataset
    self.iterations = 0
    self.keys = {}
  
  def addStat(self, stat):
    # print('addStat')
    # print(stat)
    for key in list(stat.keys()):
      if key not in self.keys:
        self.keys[key] = {}
        self.keys[key]['list'] = [stat[key]]
      else:
        self.keys[key]['list'].append(stat[key])
    self.iterations += 1
    if self.iterations == 20:
      for key in list(stat.keys()):
        self.keys[key]['avg'] = sum(self.keys[key]['list']) / len(self.keys[key]['list'])
        print(f"{key}: {self.keys[key]['avg']}")
        print(self.keys[key]['list'])

