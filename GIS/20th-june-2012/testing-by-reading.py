
from numpy import matrix
from numpy import *
from numpy.linalg import *
import numpy as np
from numpy import linalg
import math
import cmath
import json
import urllib2
import string, sys, os
import matplotlib
np.set_printoptions(precision=16)
import matplotlib.pyplot as plt

name="Thane-complete"
a=100
b=100
s=(a,b)
Z=zeros(s)

f=open(name +'krig-data.txt','r')

for i in range(a):
		nilesh=f.readline()
		gh=nilesh.split()
		for j in range(b):
			Z[i][j]=float(gh[j])

	
s=(b)
X=zeros(s)
f=open(name+'lon.txt','r')

nilesh=f.readline()
gh=nilesh.split()

for i in range(b):
	X[i]=float(gh[i])

	
s=(a)
Y=zeros(s)
f=open(name +'lat.txt','r')
nilesh=f.readline()
gh=nilesh.split()

for i in range(a):
	Y[i]=float(gh[i])

print shape(Y)
print shape(X)
print shape(Z)


CS=plt.contour(X,Y,Z,120)
plt.axis('on')
plt.clabel(CS, fontsize=1, inline=1, linewidth=0.0005, edgecolor='w')
plt.savefig(name+".png",dpi=1000,transparent=False,bbox_inches='tight')
