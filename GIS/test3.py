import numpy.matlib as M
#import numpy.matrix
from numpy import *
from numpy.linalg  import  *
size=(5,5)
A=zeros(size)

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
		
		
		
for i in range(5):
	for j in range(5):
		A[i][j]=i+j
	
print A
'''
A=array([[1,2,3],[2,3,4],[2,3,5]])
print linalg.inv(A)
'''

print multiply_mat(A,A)
