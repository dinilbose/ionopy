#This files contain basic operations
import datetime
import numpy as np
import io
from unlzw import unlzw

def get_line_number(phrase, filename):
    with open(filename) as f:
        d=list()
        for i, line in enumerate(f, 1):
            if phrase in line:
                d.append(i)
    return d

def convert_date_to_doy(sdate=''):
    """"Convert date to day of the year
    date format='%Y-%m-%d'
    example '2008-8-14'
    """
    data=datetime.datetime.strptime(sdate, '%Y-%m-%d')
    return data.strftime('%j')

def convert_doy_to_date(year='',sdoy=''):
    """"Convert day of year datetime object"""
    doy=convert_num_to_str(num=sdoy,padding=3)
    if year=='':
        print('Specify year')
        dates=[]
    else:
      dates=datetime.datetime.strptime(str(year)+str(sdoy), '%Y%j')
    return dates.strftime("%Y-%m-%d")

def convert_to_datetime(sdate=''):
    """"Convert date to date time object
    date format='%Y-%m-%d'
    example '2008-8-14'
    """
    data=datetime.datetime.strptime(sdate, '%Y-%m-%d')
    return data

def convert_num_to_str(num='',padding=''):

    if padding=='':
        print('Specify count')
    else:
        num=str(num).zfill(padding)
    return num

def set_parameter(sdate='',sdoy='',year=''):
    if (sdoy!='' and year!=''):
        sdoy_b=convert_num_to_str(num=sdoy,padding=3)
        sdate_b=convert_doy_to_date(year=year,sdoy=sdoy_b)
        year_b=convert_to_datetime(sdate_b).year
    if (sdate!=''):
        sdoy_b=convert_date_to_doy(sdate)
        year_b=convert_to_datetime(sdate).year
        sdate_b=convert_doy_to_date(year=year_b,sdoy=sdoy_b)
    if (sdoy!='' and year==''):
        print('sdoy requires year')
    return sdoy_b, sdate_b, year_b

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

def set_date_parameters(sdate='', edate='', sdoy='', edoy='', year=''):
    sdoy, sdate, year=set_parameter(sdoy=sdoy,sdate=sdate,year=year)
    if edate=='' and edoy=='':
        edate=sdate
        edoy, edate, year=set_parameter(sdoy=edoy,sdate=edate,year=year)
        #print(sdoy,edoy)
    else:
        edoy, edate, year=set_parameter(sdoy=edoy,sdate=edate,year=year)
    return sdate, edate, sdoy, edoy, year

def distance_on_unit_sphere(dlat1='',dlong1='',dlat2='',dlong2=''):
    #lat1=data.Iono_lat
    #long1=data.Iono_lon
    #lat2=data.Sbas_dlat
    #long2=data.Sbas_dlon
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    cos = (np.sin(phi1)*np.sin(phi2)*np.cos(theta1 - theta2) +
    np.cos(phi1)*np.cos(phi2))
    arc = np.arccos( cos )
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get lengthself.
    return arc


def read_Zfile(name):
    ''''Reads Z compressed file and return TEXT IO'''
    with open(name,'rb') as fh:
        compressed_data = fh.read()
        uncompressed_data = unlzw(compressed_data)
        data=io.StringIO(uncompressed_data.decode('ascii'))
    return data

