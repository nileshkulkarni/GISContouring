function makeplot(s,r)
    M=fscanfMat(s+'krig-data.txt');
    Lat=fscanfMat(s+'lat.txt');
    Lon=fscanfMat(s+'lon.txt');
    if(r=="contour")
        contour(Lat,Lon,M,20);
     else
         surf(Lat,Lon,M);
end;