#%%
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(19920613)

x = np.arange(0.0, 100.0, 5.0)
y = (x * 1.5) + np.random.rand(20) * 50

plt.scatter(x,y, c = 'b', alpha = 0.5, label = 'scatter point')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc = 'upper right')
plt.title('scatter plot')
plt.show()

# %%
