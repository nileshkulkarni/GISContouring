from numpy import matrix
from numpy import *
from numpy.linalg import *

from numpy import linalg
import math
import cmath

import matplotlib

import matplotlib.pyplot as plt



n=286 #intial itnye hi point pata hai


f = open('IITbombay.txt', 'r')
size=(300,3)
Data = zeros(size)
s=f.readline()
i=0


while(s != ""):#read karta hai file se
	k=s.split()
	Data[i][0]=float(k[0])
	Data[i][1]=float(k[1])
	Data[i][2]=float(k[2])
	i = i+1
	s=f.readline()
	
#elev_mat=[[0]*(n+1) for x in xrange(0,(n+1))]

	
# input: latlon: N*2 ndarray (N : no of points whose elevation is known), N*1 ndarraya, a ,b : dimensions of the grid)
# n=N, 

#pata wale points ka lattitude and longitude ka array hai jisme latitude 0 index pe hai aur longitude  				#chamka jayaga
size=(n,2)
latlon=zeros(size)
for i in range(n):
	latlon[i][0]= Data[i][0]
	latlon[i][1]= Data[i][1]
	
	
	 
#print latlon


latlong=[] #fart

for i in range(n):
	latlong.append([Data[i][0],Data[i][1]])
	
elevations=Data[: n][2]


s=((n+1),1)
elev_mat=ones(s)

for i in range(n):  #matrix hai yaar
	elev_mat[i]=Data[i][2]



st_lat=Data[0][0]
st_lon=Data[0][1]

temp_lat=st_lat
temp_lon=st_lon

a=50 #intne sample points 

b=50

s=(a,b,3)
grid=zeros(s)


#grid_width in degrees
lat_grid_width= 5/1

lon_grid_width=5/1


def variogram(x1,x2):   #should satisfy variogram(x,x)=0\
	l=500000/111000          # range, parameter of the exponential variogram
	#h=norm(x1-x2)
	h=((x1[0]-x2[0])**2 + (x1[1]-x2[1])**2)**0.5
	return (1-exp(-h/l))     
#: initialising array A 

s=(n+1,n+1)
A = zeros(s)
for i in range(n):
	for j in range(n):
		A[i][j]=-variogram(latlon[i],latlon[j])

for i in range(n):
	A[i][n]=1
	A[n][i]=1
	
A[n][n]=0



#*****************end of initialisation************************

#inverse of A
def multiply_mat(A,B):
	
	ra=shape(A)[0]
	ca=shape(A)[1]
	cb=shape(B)[0]
	q=(ra,cb)
	mul=zeros(q)
	for i in range(ra):
		for j in range(cb):
			sumj=0
			for k in range(ca):
				sumj = sumj+ A[i][k]*B[k][j]
			mul[i][j]=sumj
	return	mul	

	

	
A_inv = linalg.inv(A) #inverse
s=(n+1)
t=zeros(s)
#:kriging masala 
for i in range(a): #pure ek saath calculate  kia hai lol...suspense khol dia
	for j in range(b):
		for k in range(n):	
			t[k] = -variogram(array([temp_lat,temp_lon]),latlon[k])
		res = dot(A_inv,t)
		grid[i][j][0]=temp_lon
		grid[i][j][1]=temp_lat
		grid[i][j][2]=dot(res.T , elev_mat)
		temp_lon+=lon_grid_width
	temp_lat+=lat_grid_width	
	temp_lon=st_lon	 
s=(a)				
X=zeros(s)
s=(b)
Y=zeros(s)
for i in range(a):
	X[i]=grid[0,i,0]

for j in range(b):
	Y[j]=grid[j,0,1]


'''
for i in range(a):
	
	for j in range(b)
'''		
s=(a,b)
Z = zeros(s)
Z =grid[:,:,2]

X_min = min(latlon[:n,0]); X_max = max(latlon[:n,0]); 
Y_min = min(latlon[:n,1]); Y_max = max(latlon[:n,1])
#X = arange(X_min,X_max,(Y_max-Y_min)/50);	

s=(a*b)
k=0

CS=plt.contour(X,Y,Z,10)
plt.axis('off')
plt.clabel(CS, fontsize=0.05, inline=1, linewidth=0.05, edgecolor='w')
plt.savefig("IITB-contour.png",dpi=1000,transparent=False,bbox_inches='tight')


