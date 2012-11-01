from numpy import matrix
from numpy import *
from numpy.linalg import *
import scipy
from numpy import linalg
import math
import cmath

n=425 #intial itnye hi point pata hai
name='10-national-park'

f = open(name+'.txt', 'r')
size=(n,3)
Data = zeros(size)
s=f.readline()


l=0
while(s != ""):#read karta hai file se
	k=s.split()
	Data[l][0]=float(k[0])
	Data[l][1]=float(k[1])
	Data[l][2]=float(k[2])
	l = l+1
	s=f.readline()
	
#elev_mat=[[0]*(n+1) for x in xrange(0,(n+1))]

	
# input: latlon: N*2 ndarray (N : no of points whose elevation is known), N*1 ndarraya, a ,b : dimensions of the grid)
# n=N, 

#pata wale points ka lattitude and longitude ka array hai jisme latitude 0 index pe hai aur longitude  	
			#chamka jayaga
size=(n,2)
latlon=zeros(size)

for i in range(n):
	latlon[i][0]= Data[i][0]
	latlon[i][1]= Data[i][1]
	
	
	
s=((n+1),1)
elev_mat=ones(s)

for i in range(n):  #matrix hai yaar
	elev_mat[i]=Data[i][2]

def variogram(x,y): 
					#x is the a 2cross n vector contaning latitude and longitude of all n point usually 110 points.
					#y is the array of elevation 
					#Here we are trying to find the best fit line that would satisfy for differnt h's the functional value.			
	k=shape(x)[0]
	
	kc2=k*(k-1)/2				
	s=(kc2,2)
	vario_grid=ones(s)
	current_elm=0
	
	for i in range(k):
		for j in range (i+1,k):
			vario_grid[current_elm][0]=((x[i][0]-x[j][0])**2+(x[i][1]-x[j][1])**2)**0.5
			vario_grid[current_elm][1]=	((y[i]-y[j])**2)/2
			current_elm = current_elm+1
	
	#now we will find th linear best fit
	#we are solving for CX=D best fit
	
	s=(kc2,2)
	C=ones(s)
	s=(kc2,1)
	D=vario_grid[:,1]
	C[:,0]=vario_grid[:,0]
	ct=C.T
	
	ctc=dot(ct,C)
	ctci=linalg.inv(ctc)
	
	ctd=dot(ct,D)
	
	ans=dot(ctci,ctd)
	
	
	return ans
	
print variogram(latlon,elev_mat)

