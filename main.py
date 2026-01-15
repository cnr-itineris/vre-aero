#!/usr/bin/python3
#
"""
 *** Lidar data plotting routine ***
 @author: E. Lapenna
 @version 1.0 - 17-02-2025
"""
#
#
import os
import sys
import argparse
import subprocess


#
tmp_data_path = 'data/tmp/'
output_data_path = 'data/'
plot_save_folder = 'plots/'


#
def dir_set(basepath):

	# Set data directories
	global tmp_data_path
	global output_data_path
	global plot_save_folder

	# Create the nested directories if they do not exist
	os.makedirs(basepath+tmp_data_path, exist_ok=True)
	os.makedirs(basepath+output_data_path, exist_ok=True)
	os.makedirs(basepath+plot_save_folder, exist_ok=True)

	# os.path.isdir(basepath+tmp_data_path):
	if os.path.exists(basepath+tmp_data_path) and os.path.exists(basepath+output_data_path) and os.path.exists(basepath+plot_save_folder):
		#print('EXIT_SUCCESS')
		return 'EXIT_SUCCESS'
	else:
		#print('EXIT_FAILURE')
		return 'EXIT_FAILURE'

#
def check_var(value):
	if value == '5p' or value == '3p':
		#print('EXIT_SUCCESS')
		return 'EXIT_SUCCESS'
	else:
		#print('EXIT_FAILURE')
		return 'EXIT_FAILURE'

#
def main(fromDate, toDate, fromHour, toHour, station, panel, basepath):

	# Check panels option - [0]
	if dir_set(basepath) == 'EXIT_FAILURE':
		print('ERROR: unable to set working directories!')
		sys.exit()


	# Check panels option - [1]
	if check_var(panel) == 'EXIT_FAILURE':
		print('ERROR: panel mode accept "5p" and "3p" only!')
		sys.exit()


	# Call _check_data.py - [2]
	#print('_check_data.py')
	proc1 = subprocess.run(
		['python3', '_check_data.py', fromDate, toDate, station],
		capture_output=True,
		text=True
	)
	# Print result
	#print(proc1.stdout)
	if (proc1.stdout.strip() == 'EXIT_SUCCESS'):
		print('Data check... OK')
	else:
		print('ERROR: No data available!')
		sys.exit()


	# Call _get_data.py - [3]
	#print('_get_data.py')
	proc2 = subprocess.run(
		['python3', '_get_data.py', fromDate, toDate, fromHour, toHour, station, basepath],
		capture_output=True,
		text=True
	)
	# Print result
	#print(proc2.stdout)
	if (proc2.stdout.strip() == 'EXIT_SUCCESS'):
		print('Get data... OK')
	else:
		print('ERROR: No data downloaded!')
		sys.exit()


	# Call _get_data.py - [4]
	#print('_plot_elda.py')
	proc3 = subprocess.run(
		['python3', '_plot_elda.py', fromDate, toDate, fromHour, toHour, station, panel, basepath],
		capture_output=True,
		text=True
	)
	# Print result
	#print(proc3.stdout)
	if (proc3.stdout.strip() == 'EXIT_SUCCESS'):
		print('Plotting routine... OK')
	else:
		print('ERROR: Plotting failure!')
		sys.exit()


#
def parse_args():

	"""
	Parses command-line arguments for...

	Returns:
		argparse.Namespace: Parsed command-line arguments
	"""
	parser = argparse.ArgumentParser(description="""
	Download data from EARLINET...
	Arguments:\n
		obs_site (str): Observation site to analyse.\n
		obs_date_min (str): Start date in format YYYY-MM-DD.\n
		obs_date_max (str): End date in format YYYY-MM-DD.\n
		obs_hour_min (str): Start hour in format YHH:MM.\n
		obs_hour_max (str): End hour in format HH:MM.\n
		panel (str): Panel mode as '5p' or '3p'.\n

	Example usage:\n
		python3 main.py --obs_site POT --obs_date_min 2025-06-13 --obs_date_max 2025-06-13 --obs_hour_min 21:00 --obs_hour_max 23:00 --panel 5p

	""")

	parser.add_argument('--obs_site', type=str, help='Observation site', required=True)
	parser.add_argument('--obs_date_min', type=str, help='Start date', required=True)
	parser.add_argument('--obs_date_max', type=str, help='End date', required=True)
	parser.add_argument('--obs_hour_min', type=str, help='Start hour', required=True)
	parser.add_argument('--obs_hour_max', type=str, help='End hour', required=True)
	parser.add_argument('--panel', type=str, help='Panel mode', required=True)

	parser.add_argument('--basepath', type=str, help='Base output path', default='.') # implicit

	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)
	return parser.parse_args()


# Main program
if __name__ == '__main__':

	#
	args = parse_args()

	#
	station = args.obs_site
	fromDate = args.obs_date_min
	toDate = args.obs_date_max
	fromHour = args.obs_hour_min
	toHour = args.obs_hour_max
	panel = args.panel
	basepath = args.basepath

	#
	print('############################')
	print('#  Lidar profiles routine  #')
	print('############################')

	print('Observational site: '+station)
	print('Start date: '+fromDate)
	print('End date: '+toDate)
	print('Start hour: '+fromHour)
	print('End hour: '+toHour)
	print('Panel: '+panel)

	# Check implicit basepath
	#if args.basepath:
		#data_path = os.path.join(args.basepath, data_path)
		#plot_path = os.path.join(args.basepath, plot_path)

	# Check working directory, if any
	#if not os.path.exists(data_path):
	#	os.makedirs(data_path)
	#if not os.path.exists(plot_path):
	#	os.makedirs(plot_path)

	#
	main(fromDate, toDate, fromHour, toHour, station, panel, basepath)

#
#
