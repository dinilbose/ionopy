# ionopy ionex module

Ionex module helps you to download and read tec from the ionex file

List of usual institutes which provide the Ionex files are

institute=['ehrg','igsg','uqrg','esrg','codg','jplg','upcg','corg','igrg','jprg','uprg']

## Download Ionex

obs: Name of the institute

```
from ionopy.analysis import ionex

ionex.download(obs='codg',sdoy=1,edoy=20,year=2014)
```

## Reading TEC

obs : Name of the institute

lon, lat: Latitude and Logitude of the station or the location for TEC.

sdate,edate,sdoy,edoy,year : All parameters can be used

```
ionex_tec=ionex.read_tec(sdoy=1,edoy=20,obs='codg',year=2014,lat=52.379,lon=13.066)
```
lat,lon given for POTS station

Comparision plot for POTS station on 1-1-2014
![alt text](https://github.com/dinilbose/ionopy/blob/master/ionopy/documentation/Images/Tec_comparison_ionex.png)

