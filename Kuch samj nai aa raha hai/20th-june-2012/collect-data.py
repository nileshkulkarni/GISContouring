#!C:/Python27/python
# enable debugging
import json
import urllib2
from numpy import *
import numpy as np
import string, sys, os

np.set_printoptions(precision=16)
#Use this if you know all the two corners
'''
st_lat = float(sys.argv[1])
st_lon = float(sys.argv[2])
end_lat = float(sys.argv[3])
end_lon = float(sys.argv[4])
samp_rate = float(sys.argv[5])
pathtrue=sys.argv[6]
samp_rate = samp_rate*0.009'''

#Use this if you know only the latlon of the centre

c_lat = float(sys.argv[1])
c_lon = float(sys.argv[2])
area = float(sys.argv[3])
samp_rate = float(sys.argv[4])
pathtrue=sys.argv[5]
area = area/2
st_lat = c_lat + area*0.009
st_lon = c_lon + area*0.009
end_lat = c_lat - area*0.009
end_lon = c_lon - area*0.009
samp_rate = samp_rate*0.009

f3 = open(pathtrue+"_bound.txt", 'w')
f3.write(str(st_lat)+" "+str(st_lon)+"\n"+str(end_lat)+" "+str(end_lon))
f3.close()


if (st_lat<end_lat):
    temp_lat=st_lat
    st_lat=end_lat
    end_lat=temp_lat

if (st_lon>end_lon):
    temp_lon=st_lon
    st_lon=end_lon
    end_lon=temp_lon

LAT = (st_lat+end_lat)/2
LON = (st_lon+end_lon)/2
d_lat = (st_lat-end_lat)
d_lat_in_deg = d_lat/(10**5)
d_lon = (end_lon-st_lon)
d_lon_in_deg = d_lon/(10**5)



nosas_lat = int(d_lat/samp_rate) + 1
nosas_lon = int(d_lon/samp_rate) + 1
start_lat = st_lat
start_lon = st_lon


f2=open("proxies.txt")
proxy_url=f2.readline()



k=0
location_str = ''
path=pathtrue+'.txt'
f = open(path, 'w')
latitude= []
longitude= []
for i in range(nosas_lon):
    lg = start_lon + samp_rate * i
    longitude.append(lg)
for i in range(nosas_lat):
    lt = start_lat - samp_rate * i
    latitude.append(lt)
for i in range(nosas_lat):
    lt = start_lat - samp_rate * i
    for j in range(nosas_lon):
        lg = start_lon + samp_rate * j
        location_str = location_str + str(lt) + ',' + str(lg) + "|"
        k = k + 1
        if(k==25 or (i==(nosas_lat-1) and j==(nosas_lon-1))):
            url =  "http://maps.googleapis.com/maps/api/elevation/json?locations=" + location_str
            url = url.rstrip('|') + "&sensor=false"
            if len(proxy_url)!=0:
                proxy=urllib2.ProxyHandler({'http': proxy_url})
                auth = urllib2.HTTPBasicAuthHandler()
                opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
                urllib2.install_opener(opener)
            a = urllib2.urlopen(url)			
            p = json.load(a)
            results = p['results']
            length = len(results)
            e = []
            lat = []
            lng = []
            for kk in range(length):
                e.append(results[kk]['elevation'])
                latlng = results[kk]['location']
                lat.append(latlng['lat'])
                lng.append(latlng['lng'])
	    for kk in range(length):
                tstr=str(lng[kk])+'\t'+str(lat[kk])+'\t'+str(e[kk])
                for i in range(len(tstr)):
                    if(tstr[i]!=' 'and tstr[i]!='\t'and tstr[i]!='\n'):
                        lflg=1
                if(lflg==1):
                    f.write(str(lng[kk])+'\t'+str(lat[kk])+'\t'+str(e[kk])+'\n')
                lflg=0
                
	    k=0
	    location_str = ''

f.close()
