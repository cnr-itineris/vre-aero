#!/usr/bin/python3
#
"""
 *** EARLINET file download procedure ***
 @author: E. Lapenna
 @version 1.0 - 17-02-2025
"""
#
#
import os
import sys
import glob
import json
#import yaml
import requests
import zipfile
from datetime import datetime


# Set vars
#fromDayTime = '00:00' # UTC
#toDayTime = '23:59' # UTC
#ewls = '532'
#fileTypes = 'b'
levels = '1.0'

#
code_path = './opprofiles/'
tmp_data_path = './opprofiles/data/tmp/'
output_data_path = './opprofiles/data/'
plot_save_folder = './opprofiles/graphs/'


# Function to get files metadata
def get_optical_product(fromDate, toDate, fromHour, toHour, station):

	global levels

	fromDate_check = datetime.strptime(fromDate, '%Y-%m-%d')
	toDate_check = datetime.strptime(toDate, '%Y-%m-%d')

	fromHour_check = datetime.strptime(fromHour, "%H:%M")
	toHour_check = datetime.strptime(toHour, "%H:%M")

	if (fromDate_check is False) or (toDate_check is False) or (fromHour_check is False) or (toHour_check is False):
		print('EXIT_FAILURE')
		return 'EXIT_FAILURE'


	# 'https://data.earlinet.org/api...'
	url = 'https://api.actris-ares.eu/api/services/restapi/opticalproducts?'+\
		'fromDate='+fromDate+\
		'&toDate='+toDate+\
		'&fromDayTime='+fromHour+\
		'&toDayTime='+toHour+\
		'&stations='+station+\
		'&levels='+levels+\
		'&opticaltype=particledepolarization=true'

	response = requests.get(url, headers={"Accept":"application/json"})

	# Check if the response is successful
	if response.status_code == 200:
		payload = response.json()
		#print(payload)
		return payload
	else:
		return None


#
def get_optical_files(query, file_name):

	global tmp_data_path

	# Add already-present file check
	if os.path.exists(tmp_data_path+file_name):
		#print('File aready exists... continuing...')
		return file_name

	# 'https://data.earlinet.org/api...'
	url = 'https://api.actris-ares.eu/api/services/restapi/opticalproducts/downloads?filenames='+str(query)
	response = requests.get(url, headers={"Accept":"application/zip"}, stream=True)

	# Check if the response is successful
	if response.status_code == 200:
		content_type = response.headers['content-type']
		content_disposition = response.headers['content-disposition']
		temp_file = ( content_disposition.split('=', 1)[1] ).strip()
		#print(temp_file)

		with open(tmp_data_path+temp_file, 'wb') as f:
			for chunk in response.iter_content(chunk_size=8192):
				f.write(chunk)

			f.close()
			#
			#if os.path.exists(tmp_data_path+file_name):
			#	os.remove(tmp_data_path+file_name)
			#
			os.replace(tmp_data_path+temp_file, tmp_data_path+file_name) # temp_file
		return file_name # temp_file
	else:
		return None


#
def main(fromDate, toDate, fromHour, toHour, station):

	global tmp_data_path
	global output_data_path

	# Make request
	metadata = get_optical_product(fromDate, toDate, fromHour, toHour, station)
	#print(metadata)

	# Check file downloaded
	if metadata is None:
		print('EXIT_FAILURE')
		return 'EXIT_FAILURE'


	tmp_file = []
	data_query = ''

	#print('File corresponding to query parameters: ')
	for i in range(len(metadata)):
		tmp_file.append(metadata[i]['Filename'])
		#print(i, metadata[i]['ID'], metadata[i]['Filename'])

	unique_list = list(set(tmp_file)) # Remove duplicates
	data_query = ','.join(unique_list) # Create comma-separated string from list
	#print(data_query)

	# Set filename
	file_name = 'EARLINET_AerRemSen_'+station+'_'+fromDate.replace('-','')+'_'+toDate.replace('-','')+'_'+fromHour.replace(':','')+'_'+toHour.replace(':','')+'.zip'
	#print(file_name)

	# Make request
	data_file = get_optical_files(data_query, file_name)
	#print(data_file)


	if data_file is None:
		print('EXIT_FAILURE')
		return 'EXIT_FAILURE'

	# Create a pattern to match all .nc files
	pattern = os.path.join(output_data_path, '*.nc')

	# Find all .nc files in the directory
	nc_files = glob.glob(pattern)

	# Recursively delete found files
	for file_path in nc_files:
		os.remove(file_path)

	with zipfile.ZipFile(tmp_data_path+data_file, 'r') as zip_ref:
		zip_ref.extractall(output_data_path)

	# Check if files were extracted
	extr_files = os.listdir(output_data_path)
	#print(extr_files[0])

	if extr_files:
		print('EXIT_SUCCESS')
		return 'EXIT_SUCCESS'
	else:
		print('EXIT_FAILURE')
		return 'EXIT_FAILURE'


# Main program
if __name__ == '__main__':
	#
	#print('##############################')
	#print('#    Download data routine   #')
	#print('##############################')
	#
	if len(sys.argv) < 5:
		print('ERROR: Please provide enough string arguments (5)!')
	else:
		fromDate = sys.argv[1]
		toDate = sys.argv[2]
		fromHour = sys.argv[3]
		toHour = sys.argv[4]
		station = sys.argv[5]
		#basepath = sys.argv[6]
		#
		main(fromDate, toDate, fromHour, toHour, station)

#
#
