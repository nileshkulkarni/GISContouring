from numpy import matrix
from numpy import *
from numpy.linalg import *
import numpy as np
from numpy import linalg
import math
import cmath
from pylab import *
import matplotlib

import matplotlib.pyplot as plt



n=121 #intial itnye hi point pata hai


f = open('IITb.txt', 'r')
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



a=100 #itne sample points 
b=100

s=(a,b,3)
grid=zeros(s)


#grid_width in degrees
lat_grid_width= -5/11

lon_grid_width= 5/11


def variogram(x1,x2):   #should satisfy variogram(x,x)=0\
	l=500000/111000          # range, parameter of the exponential variogram
	#h=norm(x1-x2)
	h=((x1[0]-x2[0])**2 + (x1[1]-x2[1])**2)**0.5
	#return (1-exp(-h/l))     
	return 1+h


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

	

	
def krig_version1(): #:  AX=B solve karna hai na , usi ka A
	
	temp_lat=st_lat
	temp_lon=st_lon
	s=(n+1,n+1)
	A = zeros(s)
	
	#:initialising A 
	for i in range(n):
		for j in range(n):
			A[i][j]=-variogram(latlon[i],latlon[j])
		A[i][n]=1
		A[n][i]=1
	A[n][n]=0
	
	A_inv = linalg.inv(A) #inverse	
	s=(n+1)
	t=zeros(s)

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
	return 0


def krig_version2():
	temp_lat=st_lat
	temp_lon=st_lon
	s=(n+1,n+1)
	A=zeros(s) # AX=B solve kar rahe hain , aren't we? 
	s=(n+1)
	X=zeros(s)
	B=zeros(s)
	
	
	#initialising A and B
	for i in range(n):
		B[i]=elev_mat[i]
		for j in range(n):
			A[i][j]=-variogram(latlon[i],latlon[j])
		A[i][n]=1
		A[n][i]=1
	A[n][n]=0
	B[n]=0
	#************end of initialisation**************
	
			
	X=linalg.solve(A,B)		
	print X
	
	mysum=0 # sum is something pahle se, so mysum
	for i in range(a): #pure ek saath calculate  kia hai lol...suspense khol dia
		for j in range(b):
			mysum=0
			for k in range(n):
				mysum += -variogram(array([temp_lat,temp_lon]),latlon[k])*X[k]
			mysum += X[n]	 
			grid[i][j][0]=temp_lon
			grid[i][j][1]=temp_lat
			grid[i][j][2]=mysum
			temp_lon+=lon_grid_width
		temp_lat+=lat_grid_width	
		temp_lon=st_lon
	return 0
	
	
	
	
krig_version1()	
	 
s=(a)				
X=zeros(s)
s=(b)
Y=zeros(s)
for i in range(a):
	X[i]=grid[0,i,0]

for j in range(b):
	Y[j]=grid[j,0,1]



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
#show()
plt.savefig("IITB-contour.png",dpi=1000,transparent=False,bbox_inches='tight')



'''
'''

#plt.figure()


s=(a,b,3)
grid=zeros(s)

s=(a)
xlist=zeros(s)
for i in range(a):
	xlist[i]=grid[0,i,1]
s=(b)	
ylist=zeros(s)
for j in range(b):
	ylist[j]=grid[j,0,0]
s=(a,b)
Z=zeros(s)	
for i in range (a):
	for j in range(b):
		Z[i][j]=grid[i,j,2]


X_min=min(xlist)
Y_min=min(ylist)

X_max=max(xlist)
Y_max=max(ylist)

def ma(Q):
	r=shape(Q)[0]
	c=shape(Q)[1]
	ma1=Z[0][0]
	
	for i in range(r):
		for j in range(c):
			if (ma1<Q[i][j]):
				ma1=Q[i][j]
	return ma1

def mi(Q):
	r=shape(Q)[0]
	c=shape(Q)[1]
	
	mi1=Q[0][0]
	for i in range(r):
		for j in range(c):
			if (mi1>Q[i][j]):
				mi1=Q[i][j]
	return mi1

#lev=np.linspace(0,90,10)
#rint lev
X,Y = np.meshgrid(xlist, ylist)
#Z = X+Y


CS=plt.contour(X, Y, Z, 50)
plt.axis('off')
plt.clabel(CS, fontsize=3, inline=1, linewidth=3, edgecolor='w')
plt.savefig(pathtrue+".png",dpi=1000,transparent=True,bbox_inches='tight')


