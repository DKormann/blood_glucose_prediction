#%%
import csv
import matplotlib.pyplot as plt
import numpy as np

rawdata = csv.reader(open('./dataset/train.csv', 'r'))
title = next(rawdata)
rawdata = list(rawdata)

#%%
def getslice(head:str):
  member = [i for i, item in enumerate(title) if item.startswith(head)]
  return slice(member[0], member[-1]+1)

singlecolumns = ['id', 'p_num', 'time']
datacolumns = ['bg-', 'insulin', 'carbs', 'hr', 'steps', 'cals', 'activity', 'bg+']
columns = singlecolumns + datacolumns

dataslices = { col: getslice(col) for col in columns}
for col in dataslices: print(f'{col}: {", ".join(rawdata[1][dataslices[col]][:10])}')
activity_labels = list(set(act for dataline in rawdata for act in dataline[dataslices['activity']]))

data = {
  col : np.array([[float(s) if s else np.nan for s in dataline[dataslices[col]]] for dataline in rawdata[1:]])
  for col in datacolumns if col !='activity'
}

def time2int(time:str):
  h, m, s = map(int, time.split(':'))
  return h*60 + m

data['activity'] = np.array([[activity_labels.index(act) if act in activity_labels else 0 for act in raw[dataslices["activity"]]] for raw in rawdata])
data['p_num'] = np.array([dataline[dataslices['p_num']][0] for dataline in rawdata[1:]])
data['time'] = np.array([time2int(dataline[dataslices['time']][0]) for dataline in rawdata[1:]])

#%%
class Dataset:

  def __init__(self, data):
    self.data = data

  def __getattribute__(self, name: str):
    if name in ['data', 'table']: return super().__getattribute__(name)
    if name == 'bg': return self.data['bg-']
    if name == 'label': return self.data['bg+']
    return self.data[name]
  
  __slots__ = ['data', 'bg', 'insulin', 'carbs', 'hr', 'steps', 'cals', 'activity', 'activities', 'label']

  def __getitem__(self, idx):
    if isinstance(idx, str):
      return self.data[idx]
    return Dataset({col: self.data[col][idx] for col in self.data})
  
  def __repr__(self):
    return f'Dataset({len(self.bg)} samples)'

  def table(self):
    print(f'{self}:')
    for key in ['p_num', 'time']: print(f'{key}: {self.data[key][0]}')
    for key in datacolumns: print(f'{key}: {self.data[key][0][:10]}')
    print()
  

if __name__ == '__main__':
  train_data = Dataset(data)

  assert train_data.bg.shape == train_data.carbs.shape
  train_data.table()

  batch = train_data[0:10]
  print(batch)