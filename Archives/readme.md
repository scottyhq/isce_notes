# Finding SAR data for processing

## Exploring with a Jupyter notebook & python
Many archives have web interfaces that allow exporting to CSV. This folder contains a few notebooks for sorting and plotting the contents of those CSV files to quickly ascertain what to download and process.

```
conda env create -f jas.yml
source activate jas
jupyter notebook
```

## Main archives
The list below is points to the main archive hosted by the space agency of a particular satellite. 

### Sentinel-1 (S1)
https://scihub.copernicus.eu/dhus/#/home


### ERS1, ERS2, & Envisat
https://earth.esa.int/web/guest/eoli

on-demand processing and delivery of SLCs via EOLI software ("ESA's Link to Earth Observation")

### TerraSAR-X (TSX)
https://centaurus.caf.dlr.de:8443

### CosmoSkyMed (CSK)
http://87.241.31.78/index.php

### ALOS 
https://auig2.jaxa.jp/ips/home?language=en_US

### Radarsat-1 & Radarsat-2 (RS1 & RS2)
https://neodf.nrcan.gc.ca/neodf_cat3





## Mirror / Subset archives
Unfortunately most SAR data is not freely available. Some subsets of data over particular regions are hosted on mirrored archives below.

### [ASF Vertex](https://vertex.daac.asf.alaska.edu)
NASA DAAC hosting entire S1 archive, as well as some ALOS, ERS, Envisat, mostly over north america

### [GEO Supersites](http://eo-virtual-archive4.esa.int)



