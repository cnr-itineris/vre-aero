#!/usr/bin/python3
#
# Reference API: https://cds.climate.copernicus.eu/how-to-api
#

import sys
import cdsapi

def get_data(variable, sdate, edate, data_path, url=None, key=None):

    print('Downloading data... please wait...')

    dataset = "cams-global-reanalysis-eac4"
    request = {
        "variable": [variable],
        "date": [sdate+'/'+edate],
        "time": [
            "00:00", "03:00",
            "06:00", "09:00",
            "12:00", "15:00",
            "18:00", "21:00"
        ],
        "data_format": "netcdf_zip"
    }

    target = data_path+variable+'_'+sdate+'_'+edate+'.zip'

    client = cdsapi.Client(url, key)
    client.retrieve(dataset, request, target)


"""
# Test url-key
url='https://ads.atmosphere.copernicus.eu/api'
key=''

get_data('black_carbon_aerosol_optical_depth_550nm', '2022-01-15', '2022-01-20', './data', url, key)
"""
#
