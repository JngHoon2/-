#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
file_path = '../data/chipotle.tsv'
chipo = pd.read_csv(file_path, sep = '\t')

print(type(chipo))
print(chipo.shape)
print('----------------------------------------')
print(chipo.info())

print(chipo.head(10))

print(chipo.columns)
print('----------------------------------------')
print(chipo.index)

chipo['order_id'] = chipo['order_id'].astype(str)
print(chipo.describe())

print('----------------------------------------')
print(type(chipo['order_id'].unique()))

print('----------------------------------------')
print(len(chipo['order_id'].unique()))
print(len(chipo['item_name'].unique()))


print('----------------------------------------')
print(chipo['item_name'].value_counts())
print('----------------------------------------')
item_count = chipo['item_name'].value_counts()[:10]
print(type(item_count))
for idx, (val, cnt) in enumerate(item_count.iteritems(), 1):
    print('TOP ', idx, ':', val, cnt)

print('----------------------------------------')
order_count  =  chipo.groupby('item_name')['quantity'].count()
item_quantity  =  chipo.groupby('item_name')['quantity'].sum()
print(order_count[:10])
print(item_count[:10])

item_name_list = item_quantity.index.tolist()
x_pos = np.arange(len(item_name_list))
order_cnt = item_quantity.values.tolist()

plt.bar(x_pos, order_cnt, align = 'center')
plt.ylabel('ordered_item_count')
plt.title('Distribution of all orderd item')

plt.show()

print(chipo.info())
print('----------------------------------------')
print(chipo['item_price'].head())

print('----------------------------------------')
chipo['item_price'] = chipo['item_price'].apply(lambda x: float(x[1:])) 
print(chipo.describe())

chipo.groupby('order_id')['item_price'].sum().mean()
chipo.head()

# %%

# %%
