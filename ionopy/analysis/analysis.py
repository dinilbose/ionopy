#from ionopy as ionopy.filename
from ionopy.process import filename
from ionopy.process import operations as opr
import pandas as pd
import numpy as np
#opr?
def read_tec(station='',sdate='',edate='',sdoy='',edoy='',year='',obs='gps',Reciever='R',all=False):

    sdate, edate, sdoy, edoy, year=opr.set_date_parameters(sdate=sdate, edate=edate, sdoy=sdoy, edoy=edoy, year=year)
    if all:

        names=filename.load_files(station=station,year=year,filetype='tec',sat='gps')

        data=pd.DataFrame()
        for name in names:
            dat=pd.read_hdf(name)
            data=data.append(dat)
    else:
        name=filename.find_filename(filetype='tec', obs=obs,ext='',station=station, sdate=sdate, edate=edate,Reciever='R')
        data=pd.read_hdf(name)
    return data

def extract_sv(data='',sv=''):

    data=data.query('sv==@sv')
    return data


def average_daily(data=None,period='60T',output_columns=None):
    #result=day.groupby(hour).mean()
    #day.groupby(hour)
    #average=day.resample('H').mean()
    average=data.resample(period).mean()
    return average

def add_vtec(data=None,IPP=350.0*10**3):
    RE=6378.1363*10**3         #%Earth radius in meter
    #h=23000*10^3;                #%Ionospheric pierce point
    IPP=IPP
#        sine_chi= (RE*np.cos(np.deg2rad(data['Elevation'])))/(RE+IPP)
#        chi=np.arcsin(sine_chi)
#        data.loc[:, 'Vtec'] =  data['Tec']*(np.cos(chi))
    term=(RE*np.cos(np.deg2rad(data['Elevation'])))/(RE+IPP)
    Me=(1.0-term**2.0)**(1.0/2.0)
    data.loc[:, 'Vtec'] =  data['Stec']*Me
    return data
