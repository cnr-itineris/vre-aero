#!/usr/bin/python3
#

"""
 *** MAOD routine ***
 @author: E. Lapenna
 @version 1.0 - 22-01-2026
"""

import os
import sys
import json
import numpy as np
import argparse
import requests
from os.path import exists
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

#
data_path = './maod/data/'
graph_path = './maod/graphs/'
obs_list = './maod/aeronet.json'
#
aodl = 1
avg = 20

#obs_site = 'IMAA_Potenza'
#obs_date_min = '2025-01-01'
#obs_date_max = '2025-01-31'
hour_min = '00:00:00'
hour_max = '23:59:00'


#
def check_file():
	return True

#
def read_json(file):

	# Open the JSON file and load the data
	with open(file, 'r') as file:
		data = json.load(file)

	# Print only the specified keys
	#for item in data:
	#	print('['+str(item.get('id'))+'] - '+item.get('label')+', '+item.get('location')+', '+ item.get('country'))

	return data

#
def check_site(obs_site):

	# Read config file
	sites = read_json(obs_list)

	# Check if the search_string is in the labels
	exists = any(item['label'] == obs_site for item in sites)

	return exists

#
def fetch_data(url, params):

	print('Fetching data...')

	# Making the GET request with parameters
	response = requests.get(url, params=params)

	# Checking if the request was successful
	if response.status_code == 200:
		# Return the response text (plain text format)
		return response.text
	else:
		print(f"Error: {response.status_code} - {response.text}")
		return None


#
def save_file(filename, content):

	print('Creating data file...')

	with open(filename, 'w') as file:
		file.write(content)
	print(f"↳ Data saved to {filename}")


#
def read_data(file, obs_date_min, obs_date_max):

	print('Read data file...')

	data = np.genfromtxt(file, delimiter=',', skip_header=6, dtype=None, encoding='utf-8') # dtype CRUCIAL (not None)

	# Convert to a regular 2D array
	darray = np.array(data.tolist())
	#print(darray)

	# Check the shape of the data
	#print("Data shape: ", darray.shape)
	#sys.exit()

	# Extract relevant columns
	dates = darray[:, 1]  # Date column
	times = darray[:, 2]  # Time column

	aod_1064 = darray[:, 5]
	aod_1020 = darray[:, 6]
	aod_870 = darray[:, 7]
	aod_675 = darray[:, 10]
	aod_500 = darray[:, 19]
	aod_440 = darray[:, 22]
	aod_380 = darray[:, 23]
	aod_340 = darray[:, 24]

	#print(dates, times, aod_1064, aod_1020, aod_870)
	#sys.exit()


	# Combine date and time into a single datetime array
	dt_array = np.array([datetime.strptime(f"{date} {time}", "%d:%m:%Y %H:%M:%S") for date, time in zip(dates, times)])

	date_min = str(obs_date_min+' '+hour_min) # '08-01-2025 00:00:00'
	date_max = str(obs_date_max+' '+hour_max) # '08-01-2025 23:59:00'

	# Define the start and end dates for filtering
	start_date = datetime.strptime(date_min, "%Y-%m-%d %H:%M:%S")
	end_date = datetime.strptime(date_max, "%Y-%m-%d %H:%M:%S")

	# Calculate the difference in hours
	time_diff = end_date - start_date
	hours_diff = time_diff.total_seconds() // 3600  # Floor division to get whole hours

	# Filter the dataset between the specified dates
	mask = (dt_array >= start_date) & (dt_array <= end_date)


	f_dt_array = dt_array[mask].tolist()

	f_aod_1064 = list(map(float, aod_1064[mask])) # aod_1064[mask]
	f_aod_1020 = list(map(float, aod_1020[mask])) #
	f_aod_870 = list(map(float, aod_870[mask])) #
	f_aod_675 = list(map(float, aod_675[mask])) #
	f_aod_500 = list(map(float, aod_500[mask])) #
	f_aod_440 = list(map(float, aod_440[mask])) #
	f_aod_380 = list(map(float, aod_380[mask])) #
	f_aod_340 = list(map(float, aod_340[mask])) #

	# Min / max limits calc for plot
	list_array = [f_aod_1064, f_aod_1020, f_aod_870, f_aod_675, f_aod_500, f_aod_440, f_aod_380, f_aod_340]

	max_values = [max(lst) for lst in list_array]
	min_values = [min(lst) for lst in list_array]

	glob_max = max(max_values)
	glob_min = min(min_values)

	return hours_diff, glob_min, glob_max, f_dt_array, f_aod_1064, f_aod_1020, f_aod_870, f_aod_675, f_aod_500, f_aod_440, f_aod_380, f_aod_340


#
def make_plot(aods, obs_date_min, obs_date_max, image_file):

	print('Plotting...')

	hr_diff = aods[0]
	glob_min = aods[1]
	glob_max = aods[2]
	#
	f_dt_array = aods[3]
	f_aod_1064 = aods[4]
	f_aod_1020 = aods[5]
	f_aod_870 = aods[6]
	f_aod_675 = aods[7]
	f_aod_500 = aods[8]
	f_aod_440 = aods[9]
	f_aod_380 = aods[10]
	f_aod_340 = aods[11]

	# Plotting
	plt.figure(figsize=(10, 6))

	plt.plot(f_dt_array, f_aod_1064, label='AOD_1064', marker='o', linestyle='dotted')
	plt.plot(f_dt_array, f_aod_1020, label='AOD_1020', marker='*', linestyle='dotted')
	plt.plot(f_dt_array,  f_aod_870,  label='AOD_870', marker='+', linestyle='dotted')
	plt.plot(f_dt_array,  f_aod_675,  label='AOD_675', marker='x', linestyle='dotted')
	plt.plot(f_dt_array,  f_aod_500,  label='AOD_500', marker='^', linestyle='dotted')
	plt.plot(f_dt_array,  f_aod_440,  label='AOD_440', marker='v', linestyle='dotted')
	plt.plot(f_dt_array,  f_aod_380,  label='AOD_380', marker='>', linestyle='dotted')
	plt.plot(f_dt_array,  f_aod_340,  label='AOD_340', marker='<', linestyle='dotted')

	plt.title('AOD daily measures (Level 1.5)')

	plt.xlabel('Date')
	plt.ylabel('AOD')

	ymax = float(glob_max + 0.2) # Set by default

	# Convert the string to a datetime object
	date_obj_min = datetime.strptime(obs_date_min, "%Y-%m-%d")
	date_obj_max = datetime.strptime(obs_date_max, "%Y-%m-%d")

	plt.xlim(date_obj_min, date_obj_max)
	plt.ylim(0, ymax)

	# Set major ticks to show dates
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))  # Format for date and time
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))  # Set major ticks to be daily

	# Calc locator & format interval
	#hr_loc = 4 if hr_diff >= 24 else 1
	#hr_fmt = '%H' if hr_diff >= 24 else '%H:%m'

	# Set minor ticks to show every 12 hours
	plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=1))  # Set minor ticks to be every 12 hours

	# Customize minor ticks
	#plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter(hr_fmt))  # Format minor ticks to show only time


	plt.legend(title='AOD Wavelengths', loc='upper left')

	plt.xticks(rotation=45)
	plt.grid()

	plt.tight_layout()
	#plt.show()

	plt.savefig(graph_path+'AERONET_'+image_file)


#
def main(obs_site, obs_date_min, obs_date_max):

	#print('Data path: '+data_path)

	# Convert the string to a datetime object
	date_obj_min = datetime.strptime(obs_date_min, "%Y-%m-%d")
	date_obj_max = datetime.strptime(obs_date_max, "%Y-%m-%d")
	#print(date_obj_min)
	#print(date_obj_max)


	# Calculate the date difference
	date_diff = date_obj_max - date_obj_min

	# Check if date difference is greater than 30 days
	if date_diff < timedelta(days=30):
		print('ERROR: Date interval must be greater than 30 days')
		sys.exit(1)


	# Get the month number (1-12), day number (1-31), year (e.g. 2025)
	month_min = date_obj_min.month
	day_min = date_obj_min.day
	year_min = date_obj_min.year

	month_max = date_obj_max.month
	day_max = date_obj_max.day
	year_max = date_obj_max.year

	# Base URL to make the GET request to
	url = 'https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3'

	# Test parameters to be sent with the GET request
	params = {
		'site': obs_site,
		'year': year_min,
		'month': month_min,
		'day': day_min,
		'year2': year_max,
		'month2': month_max,
		'day2': day_max,
		'AOD15': '1',
		'AVG': '20',
		'if_no_html': '1'
	}

	# Set filename
	data_file = obs_site+'_'+str(date_obj_min.date())+'_'+str(date_obj_max.date())+'_'+'aod15'+'_'+'avg20'

	tmp_file = data_path+data_file+'.txt'

	# Check already download data
	if not os.path.isfile(tmp_file):
		# Fetch data
		data = fetch_data(url, params)
		if data is not None:
			#print(data)
			save_file(tmp_file, data)
	else:
		print('File already exists... proceeding...')


	# Check empty data files
	if os.path.isfile(tmp_file):
		with open(tmp_file, 'r') as file:
			line_count = sum(1 for line in file)

		if line_count <= 2:
			print('ERROR: empty data files or no data available!')
			sys.exit(1)
		else:
			print('File lenght check successful... proceeding...')
	else:
		print('ERROR: file does not exists!')
		sys.exit(1)


	# Read data form file
	aods = read_data(tmp_file, obs_date_min, obs_date_max)
	#print(aods)

	# Generate plot
	make_plot(aods, obs_date_min, obs_date_max, data_file+'.png')


#
def parse_args():

	"""
	Parses command-line arguments for Monthly Aerosol Optical Depth

	Returns:
		argparse.Namespace: Parsed command-line arguments
	"""
	parser = argparse.ArgumentParser(description="""
	This utility plots AERONET monthly AOD measurements at wavelengths 340, 380, 440, 500, 675, 870, 1012, 1064 nm.
	Arguments:\n
		obs_site (str): Observation site to analyse.\n
		obs_date_min (str): Start date in format YYYY-MM-DD.\n
		obs_date_max (str): End date in format YYYY-MM-DD.\n

	Example usage:\n
		python3 __main__.py --obs_site IMAA_Potenza --obs_date_min 2025-05-01 --obs_date_max 2025-05-31
	""")

	parser.add_argument('--obs_site', type=str, help='Observation site', required=True)
	parser.add_argument('--obs_date_min', type=str, help='Start date')
	parser.add_argument('--obs_date_max', type=str, help='End date')

	parser.add_argument('--basepath', type=str, help='Base output path', default='.') # implicit

	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)
	return parser.parse_args()


if __name__ == '__main__':

	#
	args = parse_args()

	print('')
	print('***************************')
	print('*** Monthly AOD routine ***')
	print('***************************')
	print('Observational site: '+args.obs_site)
	print('Target dates: '+args.obs_date_min+' -> '+args.obs_date_max)

	# Check implicit basepath
	if args.basepath:
		data_path = os.path.join(args.basepath, data_path)
		graph_path = os.path.join(args.basepath, graph_path)

	# Check working directory, if any
	if not os.path.exists(data_path):
		os.makedirs(data_path)
	if not os.path.exists(graph_path):
		os.makedirs(graph_path)

	# Check if site present
	if not check_site(args.obs_site):
		print('ERROR: Observation site does not exist or is not allowed!')
		sys.exit(1)

	# Call main
	main(args.obs_site, args.obs_date_min, args.obs_date_max)

#
