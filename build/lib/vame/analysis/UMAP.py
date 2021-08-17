# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:56:51 2021

@author: Jackie
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt
import umap
from sklearn.preprocessing import StandardScaler

path = r'I:\VAME_projects\minmax_LowerBach_Rightcam-Mar16-2021\model\z_array.npy'
lables_path= r'I:\VAME_projects\minmax_LowerBach_Rightcam-Mar16-2021\model\data_labels30.npy'


z= np.load(path)
lables = np.load(lables_path)

reducer = umap.UMAP()
scaled_z = StandardScaler().fit_transform(z)
embedding2 = reducer.fit_transform(scaled_z)

x = embedding2[:, 0]
y = embedding2[:, 1]
z = lables
#colors = [plt.cm.tab20(0), plt.cm.tab20b(range(0,10))]
colors2 = [plt.cm.tab20(s) for s in range(0,20,2)]
colors1 = [plt.cm.tab20b(s) for s in range(0,20)]
#colors3 = [plt.cm.tab20c(s) for s in range(0,20,2)]
colors = colors1 + colors2 
cmap=mpl.colors.ListedColormap(colors)

#cmap=plt.cm.Set1
norm = mpl.colors.BoundaryNorm(np.arange(0,31,1), cmap.N)
plt.scatter(x,y, c=z,cmap=cmap,norm=norm,s=0.1,edgecolor='none')
plt.colorbar(ticks=np.linspace(0,30,31))
plt.savefig("High resoltion_30clusters_exmp2.png",dpi=3000)
plt.show()

