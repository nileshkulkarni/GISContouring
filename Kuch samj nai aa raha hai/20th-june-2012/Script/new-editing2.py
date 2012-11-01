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

#this function takes a=mesh_height, b=mesh_width  and name of image as input

mesh_height=float(sys.argv[1])
mesh_width=float(sys.argv[2])
#contour_distance=float(sys.argv[2])#this is in meters
datafile = sys.argv[3]
name = sys.argv[4]


#name= 'IITB2'

n = 30 #intial itnye hi point pata hai


f = open(datafile, 'r')
size= (n,3)
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

	
# input: lonlat: N*2 ndarray (N : no of points whose elevation is known), N*1 ndarraya, a ,b : dimensions of the grid)
# n=N, 

#pata wale points ka lattitude and longitude ka array hai jisme latitude 0 index pe hai aur longitude  				#chamka jayaga
size=(n,2)
lonlat=zeros(size)
for i in range(n):
	lonlat[i][0]= Data[i][0]
	lonlat[i][1]= Data[i][1]
	
	

	

s=((n+1),1)
elev_mat=ones(s)

for i in range(n):  #matrix hai yaar
	elev_mat[i]=Data[i][2]


a=int(mesh_height)
b=int(mesh_width)


##st_lon=Data[0][0]

st_lat=max(Data[:,1])
st_lon=min(Data[:,0])
end_lat=min(Data[:,1])
end_lon=max(Data[:,0])


dlat =st_lat - end_lat
dlon =end_lon - st_lon

unit_distance_grid=dlat/a*111000 #this is the contouring distance in meters.
print "\n\n******************************************"
print "\n\n\nWe are Drawing conoturs at distance of " + str(unit_distance_grid) +"meters"
print "If you want yet higher resolution increase the points in mesh,increase a and b"
print "\n\n\n******************************************"

#a=100 #itne sample points #corresponding to latitude
#b=100		#corresponding to longitude

s=(a,b,3)
grid=zeros(s)


#grid_width in degrees
lat_grid_width= dlat/a

lon_grid_width=dlon/b


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
	slp = np.polyfit(vario_grid[:,0], vario_grid[:,1], 5)
	print slp
	return slp
    #return ans
#*****************end of initialisation************************

slope=variogram(lonlat,elev_mat)
print slope

def epoly(x,coeff):#yeh function polynomial ki value nikalta hai at a prticular x
	leng=shape(coeff)[0]#leng=len
	def sahayak(l):
		if (l==(leng-1)):
			return coeff[0]
		else:
			return sahayak(l+1)*x+coeff[l]
	return sahayak(0)


		
	
def distance(x,y):
	return ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5

def give_vari(x):
	return epoly(x,slope)


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
			h = distance(lonlat[i],lonlat[j])
			A[i][j]=-give_vari(h)
		A[i][n]=1
		A[n][i]=1
	A[n][n]=0
	B[n]=0
	#************end of initialisation**************
	
			
	X=linalg.solve(A,B)		
	
	
	mysum=0 # sum is something pahle se, so mysum
	for i in range(a): #pure ek saath calculate  kia hai lol...suspense khol dia
		for j in range(b):
			mysum=0
			for k in range(n):
				h = distance(array([temp_lon,temp_lat]),lonlat[k])
				mysum += - give_vari(h)*X[k]
			mysum += X[n]	 
			grid[i][j][0]=temp_lon
			grid[i][j][1]=temp_lat
			grid[i][j][2]=mysum
			temp_lon+=lon_grid_width
		temp_lat-=lat_grid_width #yaha pe nilu ne change kia tha	
		temp_lon=st_lon
	return 0
	
	
	
	
krig_version2()			 
s=(a,b)
Z=zeros(s)

f=open(name +'krig-data.txt','w')

for i in range(b):
	for j in range(a):
		Z[j][i]=(grid[j][i][2])
		f.write(str(Z[j][i])+'  ')
	f.write('\n')
	
s=(b)
X=zeros(s)
f=open(name+'lon.txt','w')

for i in range(b):
	X[i]=grid[0][i][0]
	f.write(str(X[i])+' ')

s=(a)
Y=zeros(s)
f=open(name +'lat.txt','w')

for i in range(a):
	Y[i]=grid[i][0][1]
	f.write(str(Y[i])+' ')

CS=plt.contour(X,Y,Z,20)
plt.axis('on')
plt.clabel(CS, fontsize=2, inline=1, linewidth=0.05, edgecolor='w')
plt.savefig(name+".png",dpi=1000,transparent=False,bbox_inches='tight')