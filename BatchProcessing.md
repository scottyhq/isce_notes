# Notes for batch processing Sentinel1 with topsApp.py
last update: 06/2017

ISCE version: [20170403](https://winsar.unavco.org/isce.html)

* Assumes ISCE installed and paths set up correctly. If not see notes in this folder.

## 1) Get polygon for region of interest 
from [here](http://arthur-e.github.io/Wicket/sandbox-gmaps3.html). Be sure to select 'format for URLs'. As an example, here is a square polygon surrounding the town of Ithaca, NY:
```
POLYGON((-76.59221649169922+42.515227293635355,-76.41368865966797+42.515227293635355,-76.41368865966797+42.38298910865197,-76.59221649169922+42.38298910865197,-76.59221649169922+42.515227293635355))
```

## 2) Check available data from [ASF Vertex](https://vertex.daac.asf.alaska.edu/) 
Modify the bash script below and run. Note there are a lot of search variations that you can do with instructions [here](https://www.asf.alaska.edu/get-data/api/)
```
#!/bin/bash

export PLATFORM=Sentinel-1A
#export PLATFORM=Sentinel-1B
export POLYGON="POLYGON((-76.59221649169922+42.515227293635355,-76.41368865966797+42.515227293635355,-76.41368865966797+42.38298910865197,-76.59221649169922+42.38298910865197,-76.59221649169922+42.515227293635355))"

export OUTPUT=kml 
#also csv,json,metalink

curl https://api.daac.asf.alaska.edu/services/search/param?intersectsWith=$POLYGON\&platform=$PLATFROM\&processingLevel=SLC\&output=$OUTPUT > query.$OUTPUT
```

## 3) Download all available IW SLCS 
first create a configuration file for aria2 download program
/home/CHANGE/.aria2/asf.conf 
'''
http-user=CHANGE
http-passwd=CHANGE

max-concurrent-downloads=5
check-certificate=false

allow-overwrite=false
auto-file-renaming=false
always-resume=true 
'''

for a particular track/relative Orbit modify and run bash script below
'''
#!/bin/bash

export ORBIT=106
export POLYGON="POLYGON((-76.59221649169922+42.515227293635355,-76.41368865966797+42.515227293635355,-76.41368865966797+42.38298910865197,-76.59221649169922+42.38298910865197,-76.59221649169922+42.515227293635355))"

# Sentinel-1A
curl https://api.daac.asf.alaska.edu/services/search/param?intersectsWith=$POLYGON\&platform=Sentinel-1A\&processingLevel=SLC\&beamMode=IW\&relativeOrbit=$ORBIT\&output=metalink > query$ORBIT\_S1A.metalink 

aria2c --http-auth-challenge=true --conf-path=/home/mpguest/.aria2/asf.conf  query$ORBIT\_S1A.metalink 


# Sentinel-1B
curl https://api.daac.asf.alaska.edu/services/search/param?intersectsWith=$POLYGON\&platform=Sentinel-1B\&processingLevel=SLC\&beamMode=IW\&relativeOrbit=$ORBIT\&output=metalink > query$ORBIT\_S1B.metalink 

aria2c --http-auth-challenge=true --conf-path=/home/mpguest/.aria2/asf.conf  query$ORBIT\_S1B.metalink 
'''

## Download SRTM30m 
with SNWE bounds from full IW swath range rounded to nearest integer. The command below will create the dem file needed for processing: 
'''
dem.py -c -b 41 44 -78 -74 
fixImageXml.py -f -i demLat_N41_N44_Lon_W078_W074.dem.wgs84
'''

## Download Sentinel-1 Instrument calibration files
run the following bash script
'''
#!/bin/bash
URL=https://s1qc.asf.alaska.edu/aux_cal
cd s1_auxcal
wget -r -l2 -nc -nd -np -nH -A SAFE $URL 
'''

## Download all Sentinel-1 precise orbits 
script below does not re-download existing files
'''
#!/bin/bash
URL=https://s1qc.asf.alaska.edu/aux_poeorb/
cd ./s1_poeorb
wget -r -l2 -nc -nd -np -nH -A EOF $URL
'''


## Prepare batch interferogram directories
The following will only process bursts that intersect the polygon region of interest and geocode each interferogram to matching grids witht he polygon extents. If you know you only want a specific subswath,for example IW2, use '-n 2'. To process every other pair (e.g. 24 day)use '-s 2'
'''
prep_sequential_processing.py -p ./A106 -s 1 -d  -r 42.515 42.382 -76.592 -76.413 -g 42.515 42.382 -76.592 -76.413
'''

## 4) Process all sequential pairs (e.g. 12 day)
Warning... this will take a while. the runall.py script is very basic, processing one at a time in chronological order to not use up all computer resources.
'''
runall.py
'''
