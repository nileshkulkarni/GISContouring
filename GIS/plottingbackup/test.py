import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import *

plt.figure() # Create a new figure window
xlist = np.linspace(-1.0, 1.0, 100) # Create 1-D arrays for x,y dimensions
ylist = np.linspace(-1.0, 1.0, 100)
print xlist
X,Y = np.meshgrid(xlist, ylist) # Create 2-D grid xlist,ylist values
Z = np.sqrt(X**2 + Y**2) # Compute function values on the grid
print len(X)
print shape(xlist)
print len(xlist)

plt.contour(X, Y, Z, [0.5, 1.0, 1.2, 1.5], colors = 'k', linestyles = 'solid')
plt.show()





