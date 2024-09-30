#%%
import csv
import matplotlib.pyplot as plt
import numpy as np

rawdata = csv.reader(open('./dataset/test.csv', 'r'))
rawdata = list(rawdata)

#%%

def getslice(head:str):
  member = [i for i, item in enumerate(rawdata[0]) if item.startswith(head)]
  return slice(member[0], member[-1]+1)

singlecolumns = ['id', 'p_num', 'time']
datacolumns = ['bg', 'insulin', 'carbs', 'hr', 'steps', 'cals', 'activity']
columns = singlecolumns + datacolumns

dataslices = { col: getslice(col) for col in columns}
for col in dataslices: print(f'{col}: {", ".join(rawdata[1][dataslices[col]][:10])}')

#%%

class Dataset:

  def __init__(self, data):
    self.data = data
  
  @staticmethod
  def from_rawdata(rawdata=rawdata):
    return Dataset({
      col : np.array([[float(s) if s else np.nan for s in dataline[dataslices[col]]] for dataline in rawdata[1:]])
      for col in datacolumns if col !='activity'
    })

  def __getattribute__(self, name: str):
    if name in ['data']: return super().__getattribute__(name)
    return self.data[name]
  
  __slots__ = ['data', 'bg', 'insulin', 'carbs', 'hr', 'steps', 'cals']
  

data = Dataset.from_rawdata()
assert data.bg.shape == data.carbs.shape

# %%
