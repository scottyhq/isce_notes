# ISCE/Python Cheat Sheet

A collection of common and helpful commands using ISCE, GDAL, Python
Tested with ISCE version 2 (20160908), mostly with outputs from topsApp.py

## Command Line

#### Use gdal tools on zipped Sentinel1 files
```
export FILE=S1B_IW_SLC__1SDV_20170204T160912_20170204T160940_004152_0072F4_9D51
gdalinfo /vsizip/${FILE}.zip/${FILE}.SAFE
```

#### Save unwrapped phase as single band geotiff with control over colorbar
```
isce2geotiff.py -i filt_topophase.unw.geo -o filt_topophase.unw.geo.tif -b 2 -c -10 10
```

#### Create kmz to view in Google Earth 
(Note: Google Earth Pro is now free, and can open geotifs directly, so do not really need this...)
```
gdal_translate -of KMLSUPEROVERLAY filt_topophase.unw.geo.tif filt_topophase.unw.geo.kmz
```

#### Convert unwrapped radians to displacements [m]
(Note: example for C-band Sentinel-1A Wavelength 5.55 cm)
```
gdal_calc.py -A filt_topophase.unw.geo.vrt --A_band=2 --calc="A*0.05546576/12.5663706" --outfile=filt_topophase.unw_m.geo  --format=ENVI --NoDataValue=-9999 --overwrite
```

#### East-North-Up (ENU) Cartesian vector mapping to radar Line-Of-Sight (LOS)
```
imageMath.py --eval='sin(rad(a_0))*cos(rad(a_1+90));sin(rad(a_0)) * sin(rad(a_1+90));cos(rad(a_0))' --a=los.rdr.geo -t FLOAT -s BIL -o enu.rdr.geo
```

#### Convert displacement file to UTM coordinates for modeling
if you are unsure of the UTM zone, here is a nice utility: http://www.geoplaner.com/ 
and EPSG codes can be found here: http://www.spatialreference.org/
```
gdalwarp -of VRT -t_srs EPSG:32718 filt_topophase.unw_m.geo filt_topophase.unw_m.utm
```


#### Help on particular ISCE component
```
iscehelp.py -t Sensor -a sensor=SENTINEL1
```

#### Look down an ISCE file
```
looks.py -i filt_topophase.flat -r 4 -a 4 -o filt_topophase.flat.4lks 
```

#### Get quick stats on an image
For example mean incidence and heading angles. Band 1 is incidence (radar los to surface normal), Band 2 is heading (positive clockwise from due east):
```
isce2gis.py vrt -i los.rdr.geo
gdal_edit.py -a_nodata 0.0 los.rdr.geo.vrt
gdalinfo -stats los.rdr.geo.vrt
```

#### Geocode File
```
topsApp.py —-dostep=geocode topsApp_geocodeonly.xml
```

where topApps_geocodeonly.xml has:
```
<?xml version="1.0" encoding="UTF-8"?>
<topsApp>
	<property name="geocode list">
		<value>["filt_topophase.flat.4lks"]</value>
	</property>
</topsApp> 
```


#### Unwrap specific file with Snaphu
```
```

#### Merge wrapped, geocoded, Sentinel-IW subswaths
```
gdalwarp -of ENVI -ot CFloat32 -srcnodata 0 -dstnodata 0 20160322_20160415_*/merged/*filt_topophase.flat.geo.vrt filt_topophase_merged.flat.geo.vrt
```

#### Put separate geocoded phase files on same grid (with GDAL)
note image size (-ts 450 450) can be determined from `gdalinfo filt_topophase.unw.8alks_8rlks.geo.vrt`
```
gdaltindex clipper.shp filt_topophase.unw.8alks_8rlks.geo.vrt
gdalwarp -ts 450 450 -cutline clipper.shp -crop_to_cutline /dems/demLat_S04_N12_Lon_W081_W070.dem.wgs84.vrt dem.tif
```

#### Extract wrapped phase from complex-valued files
```
isce2gis.py vrt -i filt_topophase.flat.8alks_8rlks.geo

gdal_calc.py --type Float32 -A filt_topophase.flat.8alks_8rlks.geo.vrt --calc="numpy.angle(A)" --outfile=filt_topophase.flat.8alks_8rlks.geo.phs.tif --NoDataValue=0.0 --overwrite
```

#### Create RGBA Geotiff for Google Earth
```
gdaldem color-relief -alpha filt_topophase.flat.8alks_8rlks.geo.phs.tif colors.txt filt_topophase.flat.geo.8alks_8rlks.phs.rgba.tif
```
where colors.txt is something like this:
```
-3.14   46 154 88 255
-1.57   251 255 128 255
0       224 108 31 255
1.57    200 55 55 255
3.14    215 244 244 255
nv      0   0   0   0
```

## Python Module

#### Load Processing information from PICKLE (when running insarApp.py with --steps)
```python
import isce
import pickle
with open('PICKLE/updatepreprocinfo', 'rb') as f:
    insar = pickle.load(f)
# insar is a dictionary in this case:
insar['sensor']
``` 

#### Plot array in map view and profile
```
```


## Other stuff

#### Download specific file from ASF 
```
wget https://datapool.asf.alaska.edu/SLC/SA/S1A_IW_SLC__1SSV_20141024T160957_20141024T161028_002973_003616_3171.zip
```

#### Download All Sentinel-1A SLC products for a particular point and orbit from ASF
```
export LAT=1.22
export LON=-77.37
export ORBIT=120
curl https://api.daac.asf.alaska.edu/services/search/param?intersectsWith=point%28$LON+$LAT%29\&platform=Sentinel-1A\&processingLevel=SLC\&relativeOrbit=$ORBIT\&output=metalink > query$ORBIT.metalink
aria2c --http-auth-challenge=true --conf-path=asf.conf query$ORBIT.metalink
```
Where asf.conf contains the following:
```
http-user=<CHANGE>
http-passwd=<CHANGE>
max-concurrent-downloads=5
check-certificate=false
allow-overwrite=false
auto-file-renaming=false
always-resume=true
```


