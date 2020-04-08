import numpy as np
import datetime
import logging
import io
import unlzw
from ionopy.process import filename
from ionopy.process import operations as opr
import pandas as pd
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


import os
from ftplib import FTP
import errno
#"Function _read_ionex_header and read_tec are obtained from RMExtract"


def _read_ionex_header(filep):
    """reads header from ionex file. returns data shape and position of first
    data in the file.
    Args:
        filep (filepointer) : pointer to opened ionex file.
    Returns:
        Tuple[float, np.array, np.array, np.array]:
            multiplication factor,lonarray,latarray,timearray
    """

    filep.seek(0)
    for line in filep:
        if "END OF HEADER" in line:
            break
        stripped = line.strip()
        if stripped.endswith("EPOCH OF FIRST MAP"):
            starttime = datetime.datetime(
                *(int(i) for i in
                  stripped.replace("EPOCH OF FIRST MAP","").split()))
        if stripped.endswith("EPOCH OF LAST MAP"):
            endtime = datetime.datetime(
                *(int(i) for i in
                  stripped.replace("EPOCH OF LAST MAP","").split()))
        if stripped.endswith("INTERVAL"):
            timestep = float(stripped.split()[0]) / 3600.
        if stripped.endswith("EXPONENT"):
            exponent = pow(10, float(stripped.split()[0]))
        if stripped.endswith("DLON"):
            start_lon, end_lon, step_lon = \
                (float(i) for i in stripped.split()[:3])
        if stripped.endswith("DLAT"):
            start_lat, end_lat, step_lat = \
                (float(i) for i in stripped.split()[:3])
        if stripped.endswith("OF MAPS IN FILE"):
            ntimes = int(stripped.split()[0])

    lonarray = np.arange(start_lon, end_lon + step_lon, step_lon)
    latarray = np.arange(start_lat, end_lat + step_lat, step_lat)
    dtime = endtime - starttime
    dtimef = dtime.days * 24. + dtime.seconds / 3600.
    logging.debug("timerange %f hours. step = %f ", dtimef, timestep)
    timearray = np.arange(0,
                          dtimef + timestep,
                          timestep)
    if timearray.shape[0] < ntimes:
        # bug in ILTF files,last time in header is incorrect
        extratimes = np.arange(timearray[-1] + timestep,
                               timearray[-1]
                               + (ntimes -
                                  timearray.shape[0] + 0.5) * timestep,
                               timestep)
        timearray = np.concatenate((timearray, extratimes))
    timearray += starttime.hour\
        + starttime.minute/60.\
        + starttime.second/3600.

    return exponent, lonarray, latarray, timearray


def read_tec_file(filename, _use_filter=None):
    """ returns TEC, RMS longitude, lattitude and time read from an IONEX file.
    Args:
        filename (string) : the full path to the IONEXfile
        _use_filter (float) : optional filter the data in space and time
                             with a gaussian filter with sigma use_filter.
                             calls scipy.ndimage.filter.gaussian_filter(tec,
                             use_filter)
    Returns:
        Tuple[np.array, np.array, np.array, np.array, np.array]:
            3D-arrays (time,lat,lon) of (optionally filtered) TEC and RMS +
            longitude, latitude and time array
    """
    if filename.endswith('.Z'):
        fh=open(filename,'rb')
        compressed_data = fh.read()
        ionex_file = io.StringIO(unlzw.unlzw(compressed_data).decode("ascii"))
    else:
        ionex_file = open(filename, "r")

    exponent, lonarray, latarray, timearray = _read_ionex_header(ionex_file)
    logging.info("reading data with shapes %d  x %d x %d",
                 timearray.shape[0],
                 latarray.shape[0],
                 lonarray.shape[0])
    tecarray = np.zeros(timearray.shape
                        + latarray.shape + lonarray.shape, dtype=float)
    rmsarray = np.zeros_like(tecarray)
    timeidx = 0
    lonidx = 0
    latidx = 0
    tecdata = False
    rmsdata = False
    readdata = False
    for line in ionex_file:
        if "START OF TEC MAP" in line:
            tecdata = True
            rmsdata = False
            timeidx = int(line.strip().split()[0]) - 1
            continue
        if "START OF RMS MAP" in line:
            rmsdata = True
            tecdata = False
            timeidx = int(line.strip().split()[0]) - 1
            continue
        if "LAT/LON1/LON2/DLON/H" in line:
            readdata = True
            latstr = line.strip().replace("LAT/LON1/LON2/DLON/H","")
            lat = np.fromstring(" -".join(latstr.split("-")), sep=" ")
            latidx = np.argmin(np.abs(latarray - lat[0]))
            lonidx = 0
            continue
        if tecdata and ("END OF TEC MAP" in line):
            readdata = False
            continue
        if rmsdata and ("END OF RMS MAP" in line):
            readdata = False
            continue
        if readdata:
            data = np.fromstring(" -".join(line.strip().split("-")),
                                 sep=" ") * exponent
            if tecdata:
                tecarray[timeidx, latidx, lonidx:lonidx + data.shape[0]] = data
            elif rmsdata:
                rmsarray[timeidx, latidx, lonidx:lonidx + data.shape[0]] = data
            lonidx += data.shape[0]
    if not _use_filter is None:
        tecarray = myfilter.gaussian_filter(
            tecarray, _use_filter, mode='nearest')
    return tecarray, rmsarray, lonarray, latarray, timearray

def nearest_points(data,value):
    return (abs(data-value)).argmin()

def nearest_tec(filename='',time=[],lon=[],lat=[],display=True):
    """Find nearest tec from the ionex file. It does not do any interpolation
    Input filename
    desired time,lat,long
    output time and tec

    """
    tecarray, rmsarray, lonarray, latarray, timearray=read_tec_file(filename)
    lon_idx=nearest_points(lonarray,float(lon))
    lat_idx=nearest_points(latarray,float(lat))
    if display:
        print('Nearest Lat:',latarray[lat_idx],'Lon',lonarray[lon_idx])
    if time==[]:
        tec=tecarray[:,lat_idx,lon_idx]
    else:
        time_idx=nearest_points(timearray,float(time))
        tec=tecarray[:,lat_idx,lon_idx]
    return timearray,tec

def read_tec(sdoy='',edoy='',sdate='',edate='',year='',obs='codg',lat='',lon='',ax=None,legend=True):
    """
    Reads TEC from Ionex file. For a specfic lattitude and longitude.

    obs=['ehrg','igsg','uqrg','esrg','codg','jplg','upcg','corg','igrg','jprg','uprg']

    """

    sdate, edate, sdoy, edoy, year=opr.set_date_parameters(sdate=sdate, edate=edate, sdoy=sdoy, edoy=edoy, year=year)
    Data_whole=pd.DataFrame()
    #print('hii')
    for doy in range(int(sdoy),int(edoy)+1):

        doy, date, year=opr.set_parameter(sdoy=doy,year=year)
        #print(doy,year,date)
        ionex_name=filename.find_filename(filetype='ionex',obs=obs,sdate=date,year=year)

#    for ins in institute:
        #files='/home/dlab/Desktop/Project/ionopy/test/ionex/'+i
        time,tec=nearest_tec(filename=ionex_name,lat=lat,lon=lon,display=False)
        ff=str((24/(len(time)-1)))+'H'
        f=len(time)
        #print(f)
        a=pd.date_range(date,periods=f,freq=ff)
        b=a.to_frame()
        b['Ionex_vtec']=tec
        del b[0]
        b['Lat']=lat
        b['Lon']=lon

        Data_whole=Data_whole.append(b)
        #b.ionex_tec.plot(label=ins,legend=legend,ax=ax)
    Data_whole=Data_whole.loc[~Data_whole.index.duplicated(keep='first')]
    return Data_whole


def download(obs='',sdate='',edate='',sdoy='',edoy='',year='',Reciever='R'):

    #Initial settings
    if edate == '' and edoy=='':
        date_string='Y'
        sdate, edate, sdoy, edoy, year=opr.set_date_parameters(sdate=sdate, edate=edate, sdoy=sdoy, edoy=edoy, year=year)
    else:
        sdate, edate, sdoy, edoy, year=opr.set_date_parameters(sdate=sdate, edate=edate, sdoy=sdoy, edoy=edoy, year=year)

    #Path creation
    names=filename.find_filename(filetype='ionex',obs=obs,sdate=sdate)
    path=os.path.dirname(names)
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        else:
            print ("Already exist %s " % path)
        pass

    #new="ftp://cddis.nasa.gov/gnss/products/ionex/20$yearshort/$lday/$i"$lday"0."$yearshort"i.Z"


    ftp = FTP("cddis.nasa.gov","anonymous","anonymous")

    #File download
    for doy in range(int(sdoy),int(edoy)+1):

        doy, date, year=opr.set_parameter(sdoy=doy,year=year)
        doy_str=opr.convert_num_to_str(num=doy,padding=3)
        year_short=str(year)[-2:]
        nam=filename.find_filename(filetype='ionex',obs=obs,sdate=date,pathname=False)

        file_name='gnss/products/ionex/'+str(year)+'/'+doy_str+'/'+nam
        names=filename.find_filename(filetype='ionex',obs=obs,sdate=date)
        print(names)
        if not os.path.isfile(names):
            try:
                ftp.retrbinary("RETR " + file_name ,open(names, 'wb').write)
            except:
                print("Error in download "+names)

                if os.stat(names).st_size==0:
                    os.remove(names)



