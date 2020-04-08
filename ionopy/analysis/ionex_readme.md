# ionopy ionex module

Ionex module helps you to download and read tec from the ionex file

List of usual institutes which provide the Ionex files are

institute=['ehrg','igsg','uqrg','esrg','codg','jplg','upcg','corg','igrg','jprg','uprg']

## Download Ionex

obs: Name of the institute

```
from ionopy.analysis import ionex

ionex.download(obs='codg',sdoy=1,edoy=20,year=2017)
```

## Reading TEC

obs : Name of the institute

lon, lat: Latitude and Logitude of the station or the location for TEC.

sdate,edate,sdoy,edoy,year : All parameters can be used

```
ionex_tec=ionex.read_tec(sdoy=1,edoy=20,obs='uqrg',year=2017,lon=10,lat=10)
```
