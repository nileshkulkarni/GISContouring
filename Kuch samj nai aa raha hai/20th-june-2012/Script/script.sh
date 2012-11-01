#!/bin/bash
echo "Hello, "$USER". Welcome to ContourPlotting Routine."
a=0
b=0
lat=0
lon=0
area=0
sampleRate=0

echo -n "Do you want to collect data and then  krig : "
read  choice	

if [ "$choice" == "y" ]; then
	echo -n " Please enter the latitude >  "
	read lat;
	echo -n " Please enter the longitude > "
	read lon;
	echo -n " Please enter the area > "
	read area;
	echo -n " Please enter the sampling rate > "
	read sampleRate;
	echo -n " Please enter the file name onto which you want to write your data  > "
	read filename;

	echo "Processing you request collecting data from Google Elevation API"
	python collect-data.py $lat $lon $area $sampleRate $filename

	echo "Data Successfully collected"
	echo " Will start krigging the data"
	
	echo -n "Please enter the mesh height > "
	read a
	echo -n "Please enter the mesh widht > "
	read b
	X = $filename + ".txt"
	python new-editing2.py $a $b "$X" "$filename"
	echo "Processing  Done"
	Y = $filename+ ".png"
	shotwell $Y


else 
	echo " Will start krigging the data"
	
	echo -n "Please enter the mesh height > "
	read a
	echo -n "Please enter the mesh width > "
	read b
	echo -n "Please enter the name of file where data is collected > "
	read data
	echo -n "Please enter the name you want to output data to > "
	read filename
	python new-editing2.py $a $b "$data" "$filename" 
	
	echo "Processing  Done"
#	Y = $filename + ".png"
#	shotwell Y


fi

