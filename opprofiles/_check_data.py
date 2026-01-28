#!/usr/bin/python3
#

#
import os
import sys
import requests
import zipfile
from datetime import datetime
#

# Function to get files metadata
def get_optical_product(fromDate, toDate, station):

	fromDate_check = datetime.strptime(fromDate, '%Y-%m-%d')
	toDate_check = datetime.strptime(toDate, '%Y-%m-%d')

	if (fromDate_check is False) or (toDate_check is False):
		print('EXIT_FAILURE')
		return 'EXIT_FAILURE'
		sys.exit()

	# 'https://data.earlinet.org/api...'
	url = 'https://api.actris-ares.eu/api/services/restapi/products/metadata/OPTICAL?'+\
		'fromDate='+fromDate+\
		'&toDate='+toDate+\
		'&stations='+station+\
		'&opticaltype=particledepolarization=true' # ???
	response = requests.get(url, headers={"Accept":"application/json"})

	# Check if the response is successful
	if response.status_code == 200:
		payload = response.json()
		return payload
	else:
		return None


# Main function
def main(fromDate, toDate, station):
	# Make request
	metadata = get_optical_product(fromDate, toDate, station)

	if metadata is None:
		print('EXIT_FAILURE')
		return 'EXIT_FAILURE'
		sys.exit()

	files_array = []

	#print('File corresponding to query parameters: ')
	for i in range(len(metadata)):
		# Filter for wavelenght 532 and file type 'b'
		#if (metadata[i]['Emission Wavelength']['Value'] == 532 and metadata[i]['File Type']['Code'] == 'b'):
		files_array.append(metadata[i]['ID'])
		#print(i, metadata[i]['Filename']) # metadata[i]['Emission Wavelength']['Value'], metadata[i]['File Type']['Code']

	#print('Files found: '+str(len(files_array)))

	if (len(files_array) >= 0):
		print('EXIT_SUCCESS')
		return 'EXIT_SUCCESS'

# https://java2blog.com/bash-get-output-from-python-script/

# Main program
if __name__ == '__main__':
	#
	#print('##############################')
	#print('#     Check data routine     #')
	#print('##############################')
	#
	if len(sys.argv) < 3:
		print('ERROR: Please provide enough string arguments (3)!')
	else:
		fromDate = sys.argv[1]
		toDate = sys.argv[2]
		station = sys.argv[3]
		#
		#print('Checking for dates: '+fromDate+' -> '+toDate+', station: '+station)
		main(fromDate, toDate, station)

#
#

