import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# 生成X和Y的数据
X=np.arange(-5,5,0.1)
Y=np.arange(-5,5,0.1)
X,Y=np.meshgrid(X,Y)

# 目标函数
Z=X**2+Y**2+X

# 绘图
fig=plt.figure()
ax=Axes3D(fig)
surf=ax.plot_surface(X,Y,Z,cmap=cm.coolwarm)
plt.show()

