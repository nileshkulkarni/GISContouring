
X_min = min(x[:,0]); X_max = max(x[:,0]); Y_min = min(x[:,1]); Y_max = max(x[:,1])
X = arange(X_min,X_max,(X_max-X_min)/50);	X = append(X,X_max)
Y = arange(Y_min,Y_max,(Y_max-Y_min)/50);	Y = append(Y,Y_max)
Z = grid_kriging(x[:,0:2],x[:,2],X,Y)

CS=plt.contour(X, Y, Z, 50)
plt.axis('off')
plt.clabel(CS, fontsize=3, inline=1, linewidth=3, edgecolor='w')
plt.savefig(pathtrue+".png",dpi=1000,transparent=True,bbox_inches='tight')

