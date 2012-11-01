import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import *



plt.figure()

s=(a)
xlist=zeros(a)
for i in range(a):
	xlist[i]=grid[0,:,1]
	
for j in range(b):
	ylist[i]=grid[:,0,0]
s=(a,b)
Z=zeros(a,b)	
for i in range (a):
	for j in range(b):
		Z[i][j]=grid[i,j,2]

X_min=min(xlist)
Y_min=min(ylist)

X_max=max(xlist)
Y_max=max(ylist)

def ma(Z):
	r=shape(Z)[0]
	c=shape(Z)[1]
	ma=Z[0][0]
	
	for i in range(r)
		for j in range(c)
			if (ma<Z[i][j]):
				ma=Z[i][j]
	return ma

def mi(Z):
	r=shape(Z)[0]
	c=shape(Z)[1]
	
	mi=Z[0][0]
	for i in range(r)
		for j in range(c)
			if (mi>Z[i][j]):
				mi=Z[i][j]
	return mi

lev=np.linspace(mi,ma,10)

X,Y = np.meshgrid(xlist, ylist)

plt.contour(X, Y, Z,lev, colors = 'k', linestyles = 'solid')
plt.show()
	

