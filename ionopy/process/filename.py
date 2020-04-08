#import numpy as np
#from . import operations
#import ionopy.process.operations as opr
from ionopy.process import operations as opr
#import ./operations as opr
import pandas as pd
import os

from os.path import expanduser
home = expanduser("~")

Data_Repository='/home/dlab/Desktop/Project/sba02/Data'
#Data_Repository='/media/dlab/Datadisk/Germany/Data'

Data_Repository=home+'/Data_ionopy'


#Data_Repository='/media/dlab/Datadisk/sba02/Data'

#def station_name(station=''):


#    return name

def find_filename(filetype='', obs='mixed',sat='',ext='',station='',sdate='',edate='',sdoy='',edoy='',year='',Reciever='R',short=False,pathname=True):
    station=station.upper()

    station_name=station+'_'+Reciever

    if edate == '' and edoy=='':
        date_string='Y'
        sdate, edate, sdoy, edoy, year=opr.set_date_parameters(sdate=sdate, edate=edate, sdoy=sdoy, edoy=edoy, year=year)
    else:
        sdate, edate, sdoy, edoy, year=opr.set_date_parameters(sdate=sdate, edate=edate, sdoy=sdoy, edoy=edoy, year=year)
        date_string=str(sdoy)+'D'+str(edoy)


    F={"DCB":'DCB',"rinex":'.rnx',"mixed":'M',"meas":'MEAS',"navigation":'N',"observation":'O',"sinex":'.BSX',"hantaka":'.crx'}
    satlist={"mixed":'M',"gps":'G',"sbas":'S',"glonass":'R',"Galileo":'E',"beidou":'C',"qzss":'J',"irnss":'I'}

    if sat!='':

        satlist[obs]=satlist[obs]+str(sat)

    if filetype=='rinex':

        name=station_name+'_'+str(year)+str(sdoy)+'0000'+'_'+'01D'+'_'+'30S'+'_'+satlist[obs]+'O'+F[filetype]
        path_name=Data_Repository+'/'+str(year)+'/'+'Rinex'+'/'+station+'/'+name

    if filetype=='rinex2':
        station_name=station.lower()
        year_short=str(year)[-2:]
        name=station_name+str(sdoy)+'0.'+year_short+'o.Z'
        path_name=Data_Repository+'/'+str(year)+'/'+'Rinex2'+'/'+station_name+'/'+name


    if filetype=='hantaka':

        name=station_name+'_'+str(year)+str(sdoy)+'0000'+'_'+'01D'+'_'+'30S'+'_'+satlist[obs]+'O'+F[filetype]
        path_name=Data_Repository+'/'+str(year)+'/'+'Rinex'+'/'+station+'/'+name

    if filetype=='navigation':
        y=str(year)
        name='brdc'+str(sdoy)+'0.'+y[2:]+'n.Z'
        path_name=Data_Repository+'/'+str(year)+'/'+'Navigation'+'/'+name


    if filetype=='sinex':

        #CAS0MGXRAP_20170010000_01D_01D_DCB.BSX
        name='CAS0MGXRAP'+'_'+str(year)+str(sdoy)+'0000'+'_'+'01D_01D_'+'DCB'+F[filetype]
        if ext=='hdf':
            name='CAS0MGXRAP'+'_'+str(year)+str(sdoy)+'0000'+'_'+'01D_01D_'+'DCB'+'.hdf'

        path_name=Data_Repository+'/'+str(year)+'/'+'Dcb'+'/'+name

    if filetype=='dcb':
        year_short=str(year)[-2:]
        month=sdate[5:7]
        if station=='P1P2':

            name='P1P2'+year_short+month+'_ALL.DCB.Z'

        if station=='P1C1':

            name='P1C1'+year_short+month+'_ALL.DCB.Z'

        path_name=Data_Repository+'/'+str(year)+'/'+'Dcb'+'/'+'CODE/'+name

    if filetype=='meas':

        name=station_name+'_'+str(year)+'_'+date_string+'_'+satlist[obs]+'M'+'.hdf'

        path_name=Data_Repository+'/'+str(year)+'/'+'Meas'+'/'+name

    if filetype=='tec':

        name=station_name+'_'+str(year)+'_'+date_string+'_'+satlist[obs]+'T'+'.hdf'

        path_name=Data_Repository+'/'+str(year)+'/'+'Tec'+'/'+name

    if filetype=='ionex':
        name=obs+str(sdoy)+'0.'+str(year)[-2:]+'i'+'.Z'
        path_name=Data_Repository+'/'+str(year)+'/'+'Ionex'+'/'+obs+'/'+name
    if pathname:
        name=path_name

    return name

        #SGOC00LKA_R_20170920000_01D_30S_MO.rnx

def load_files(filetype='', obs='mixed',sat='',ext='',station='',sdate='',edate='',sdoy='',edoy='',year='',Reciever='R',short=False,pathname=True):

    F={"DCB":'DCB',"rinex":'.rnx',"mixed":'M',"meas":'M',"navigation":'N',"observation":'O',"sinex":'.BSX',"hantaka":'.crx','tec':'T'}
    satlist={"mixed":'M',"gps":'G',"sbas":'S',"glonass":'R',"Galileo":'E',"beidou":'C',"qzss":'J',"irnss":'I'}

    station=station.upper()
    prefixed = [filename for filename in os.listdir('.') if filename.startswith(station) and filename.endswith("GM.hdf")]

    if filetype=='meas':

    #name=station_name+'_'+str(year)+'_'+date_string+'_'+satlist[obs]+'M'+'.hdf'
        path=Data_Repository+'/'+str(year)+'/'+'Meas'

        new=satlist[sat]+'M'+'.hdf'
        #print(new)
        name = [filename for filename in os.listdir(path) if filename.startswith(station) and filename.endswith(new)]
        path_name=[path+'/' + x for x in name]


    if filetype=='tec':
        path=Data_Repository+'/'+str(year)+'/'+'Tec'
        new=satlist[sat]+'T'+'.hdf'
        #print(new)
        name = [filename for filename in os.listdir(path) if filename.startswith(station) and filename.endswith(new)]
        path_name=[path+'/' + x for x in name]


    if filetype=='ionex':
        path=Data_Repository+'/'+str(year)+'/'+'Ionex'+'/'+obs
        new=str(year)[2:4]+'i'
        #print(new)
        name = [filename for filename in os.listdir(path) if filename.startswith(obs) and filename.endswith(new)]
        path_name=[path+'/' + x for x in name]

    if pathname:
        name=path_name
    name.sort()
    return name

