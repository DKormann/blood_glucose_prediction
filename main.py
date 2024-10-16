#%%
import matplotlib.pyplot as plt
from dataloader import Dataset, data
import numpy as np
train_data = Dataset(data)

#%%

plt.imshow(train_data.bg, aspect='auto')
#%%

plt.imshow(train_data.activity, aspect='auto')
#%%
train_data.steps[idxs[0][-5]]
# %%
plt.plot((1-np.isnan(train_data.steps)).sum(1)[:1000])
# %%

train_data.label.shape

#%%

len(set(train_data.p_num))


