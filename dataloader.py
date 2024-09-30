#%%
import csv
import matplotlib.pyplot as plt
import numpy as np

rawdata = csv.reader(open('./dataset/test.csv', 'r'))
title = next(rawdata)
rawdata = list(rawdata)

#%%

def getslice(head:str):
  member = [i for i, item in enumerate(title) if item.startswith(head)]
  return slice(member[0], member[-1]+1)

singlecolumns = ['id', 'p_num', 'time']
datacolumns = ['bg', 'insulin', 'carbs', 'hr', 'steps', 'cals', 'activity']
columns = singlecolumns + datacolumns

dataslices = { col: getslice(col) for col in columns}
for col in dataslices: print(f'{col}: {", ".join(rawdata[1][dataslices[col]][:10])}')

#%%
activity_labels = list(set(act for dataline in rawdata for act in dataline[dataslices['activity']]))

data = {
  col : np.array([[float(s) if s else np.nan for s in dataline[dataslices[col]]] for dataline in rawdata[1:]])
  for col in datacolumns if col !='activity'
}

data['activities'] = np.array([[activity_labels.index(act) if act in activity_labels else 0 for act in raw[dataslices["activity"]]] for raw in rawdata])

for col in singlecolumns: data[col] = np.array([dataline[dataslices[col]][0] for dataline in rawdata[1:]])

#%%
class Dataset:

  def __init__(self, data):
    self.data = data

  def __getattribute__(self, name: str):
    if name in ['data']: return super().__getattribute__(name)
    return self.data[name]
  
  __slots__ = ['data', 'bg', 'insulin', 'carbs', 'hr', 'steps', 'cals', 'activity', 'activities']
  
train_data = Dataset(data)
assert train_data.bg.shape == train_data.carbs.shape
