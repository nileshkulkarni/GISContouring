from numpy import *

s=(2,2)

grid=zeros(s)

grid[0][0]=1
grid[0][1]=2
grid[1][0]=3
grid[1][1]=4


f=open('IITb-2500-data.txt','w')

for i in range(2):
	for j in range(2):
		f.write(str(grid[i][j])+'\t')
	
	f.write('\n')
