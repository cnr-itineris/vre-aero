#!/usr/bin/python3
#

"""
 *** DOD routine ***
 @author: E. Lapenna
 @version 1.0 - 22-01-2026
"""

import os
import sys
import numpy as np
import argparse
import netCDF4 as nc
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# Set variables
data_path = './dod/data/'
plot_path = './dod/graphs/'


def plot(obs_site, DT):

	global data_path
	global plot_path

	# Carica AERONET DOD 500, 551 & 555nm (recuperato da AE_440-870) Tutti i punti
	dataset = nc.Dataset(data_path + 'AERONET_'+obs_site+'_lv20_15.nc')
	ts_aero_aeDT = dataset.variables['DATETIME'][:]
	ts_aero_aeDO = dataset.variables['DOD'][:]
	ts_aero_aeLV = dataset.variables['LEVEL'][:]
	ts_aero_aeWL = dataset.variables['WAVELENGTH'][:]

	#print(ts_aero_aeDT)
	#sys.exit()

	# Carica AERONET COARSE_AOD_500 Tutti i punti
	dataset = nc.Dataset(data_path + 'AERONET_'+obs_site+'ONEILL_lv20_15.nc')
	ts_aero_coDT = dataset.variables['DATETIME'][:]
	ts_aero_coCO = dataset.variables['DOD'][:] # CAOD_500
	ts_aero_coLV = dataset.variables['LEVEL'][:]

	#print(ts_aero_coDT)
	#sys.exit()

	# Carica WMO MULTIMODEL DOD_550 TIME-SERIES
	dataset = nc.Dataset(data_path + 'WMO_MULTIMODEL_'+obs_site+'_2012-202405.nc')
	ts_modelDT = dataset.variables['DATETIME'][:] # dt_12_24_3h
	ts_modelDOD = dataset.variables['DOD'][:] # OD550_DUST

	#print(ts_modelDT)
	#sys.exit()

	# Carica MONARCH REANALYSIS DOD_550 TIME-SERIES
	dataset = nc.Dataset(data_path + 'MONARCH_Reanalysis_'+obs_site+'_2007-2016.nc')
	ts_monarchDT = dataset.variables['DATETIME'][:] # dt_07_16_3h
	ts_monarchDOD = dataset.variables['DOD'][:] # DODavs

	#print(ts_monarchDT)
	#sys.exit()


	# Formato di input: Y,M,D,H,MI,S (MI & S sempre 0)
	#DT = datetime(2014, 9, 24, 18, 0, 0) # (2013, 9, 5, 6, 0, 0)
	dt_week_start = DT - timedelta(days=1.5)
	dt_week_end = DT + timedelta(days=1.5)
	fake_DT = np.arange(dt_week_start, dt_week_end, timedelta(hours=3)).astype(datetime)


	# Trova gli indici per i dati corrispondenti
	#inaero_aeDT = np.where((ts_aero_aeDT >= dt_week_start) & (ts_aero_aeDT <= dt_week_end))[0]
	#
	inaero_aeDT = np.where( (ts_aero_aeDT >= dt_week_start.timestamp()) & (ts_aero_aeDT <= dt_week_end.timestamp()) )
	inaero_coDT = np.where( (ts_aero_coDT >= dt_week_start.timestamp()) & (ts_aero_coDT <= dt_week_end.timestamp()) )
	inmodelDT = np.where( (ts_modelDT >= dt_week_start.timestamp()) & (ts_modelDT <= dt_week_end.timestamp()) )
	inmonarchDT = np.where( (ts_monarchDT >= dt_week_start.timestamp()) & (ts_monarchDT <= dt_week_end.timestamp()) )

	#print(inaero_aeDT, inaero_coDT, inmodelDT, inmonarchDT)
	#sys.exit()


	# Plot
	plt.figure(1)

	#
	plt.grid(True)

	"""
	plt.rcParams['figure.figsize'] = [10.44, 5.54]
	plt.rcParams['figure.subplot.left'] = 0.05
	plt.rcParams['figure.subplot.right'] = 0.95
	"""

	### AERONET DOD ###
	if inaero_aeDT:
		plt.plot(ts_aero_aeDT[inaero_aeDT], ts_aero_aeDO[inaero_aeDT], marker='o', linestyle='--') # X, Y, markersize=8
	else:
		plt.plot(fake_DT, np.full(fake_DT.shape, np.nan), marker='o', linestyle='--')

	### AERONET COARSE ###
	if inaero_coDT:
		plt.plot(ts_aero_coDT[inaero_coDT], ts_aero_coCO[inaero_coDT], marker='o', linestyle='--') # X, Y
	else:
		plt.plot(fake_DT, np.full(fake_DT.shape, np.nan), marker='o', linestyle='--')

	### MONARCH ###
	if inmonarchDT: # .size > 0
		plt.plot(ts_monarchDT[inmonarchDT], ts_monarchDOD[inmonarchDT], marker='o', linestyle='--') # X, Y
	else:
		plt.plot(fake_DT, np.full(fake_DT.shape, np.nan), marker='o', linestyle='--')

	### WMO ###
	if inmodelDT: # .size > 0
		plt.plot(ts_modelDT[inmodelDT], ts_modelDOD[inmodelDT], marker='o', linestyle='--') # X, Y
	else:
		plt.plot(fake_DT, np.full(fake_DT.shape, np.nan), marker='o', linestyle='--')


	#plt.hold(False)
	plt.xlim()
	#plt.xlim([dt_week_start, dt_week_end])
	#plt.xlim([min(ts_aero_aeDT[inaero_aeDT].tolist()), max(ts_aero_aeDT[inaero_aeDT].tolist())])
	#
	plt.xticks([dt_week_start.timestamp(), (DT - timedelta(days=1.0)).timestamp(), (DT - timedelta(days=0.5)).timestamp(), DT.timestamp(), (DT + timedelta(days=0.5)).timestamp(), (DT + timedelta(days=1.0)).timestamp(), dt_week_end.timestamp()],
			['-36 h', '-24 h', '-12 h', '0 h', '+12 h', '+24 h', '+36 h']) # '-36 h', '-12 h', DT.strftime('%Y-%m-%d %H:%M:%S'), '+12 h', '+36 h'
	#
	plt.legend(
		['AERONET DOD ' + ', '.join(map(str, np.unique(ts_aero_aeWL[inaero_aeDT]))) + 'nm, lv' + ', '.join(map(str, np.unique(ts_aero_aeLV[inaero_aeDT]))),
		'AERONET COARSE AOD 500nm, lv' + ', '.join(map(str, np.unique(ts_aero_coLV[inaero_coDT]))),
		'MONARCH Reanalysis DOD 550nm',
		'WMO MULTI-MODEL DOD 550nm'],
		loc='upper right') # Legend position
	#

	plt.ylim([0, 1.2]) # [0, 1]

	plt.xlabel(DT)
	plt.ylabel('DOD')
	plt.gca().fontsize = 15
	plt.title(obs_site)

	#plt.show()

	plot_file = plot_path + obs_site+'_'+ str(datetime.strftime(DT, "%Y-%m-%d_%H%M")) + '.png'

	# Check if plot already exists
	if os.path.exists(plot_file):
		# If it exists, delete the file
		os.remove(plot_file)

	plt.savefig(plot_file)


#
def main(obs_site, obs_date, obs_hour):

	# Check site
	if not (obs_site == "IMAA_Potenza" or obs_site == "Ispra" or obs_site == "Lamezia_Terme"):
		print(f"ERROR: {obs_site} is not equal to IMAA_Potenza or Ispra.")
		sys.exit(1)

	# Check date format
	if not datetime.strptime(obs_date, "%Y-%m-%d"):
		print(f"ERROR: {obs_date} is not a valid date.")
		sys.exit(1)

	# Check hour format
	if not datetime.strptime(obs_hour, "%H:%M"):
		print(f"ERROR: {obs_hour} is not a valid time.")
		sys.exit(1)


	# Convert to datetime object
	dt = datetime.strptime(f"{obs_date} {obs_hour}", "%Y-%m-%d %H:%M")

	# Define the comparison dates
	start_date = datetime(2007, 1, 1)
	end_date = datetime(2024, 12, 31)

	# Check if the datetime_obj is within the range
	if not (start_date < dt < end_date):
		print("DT outside range")


	plot(obs_site, dt)

#
def parse_args():

	"""
	Parses command-line arguments for DOD Time Series

	Returns:
		argparse.Namespace: Parsed command-line arguments
	"""
	parser = argparse.ArgumentParser(description="""
	This utility uses AERONET, WMO and MONARCH data to visualize hourly dust optical depths measurements for a specific date time (computed from -36hr to +36hr from user inputs) at measurement sites.
	Arguments:\n
		obs_site (str): Observation site to analyse.\n
		obs_date (str): Observation date in format YYYY-MM-DD.\n
		obs_date (str): Observation date in format HH:MM.\n

	Example usage:\n
		python3 __main__.py --obs_site IMAA_Potenza --obs_date 2014-09-24 --obs_hour 10:00
	""")

	parser.add_argument('--obs_site', type=str, help='Observation site', required=True)
	parser.add_argument('--obs_date', type=str, help='Observation date', required=True)
	parser.add_argument('--obs_hour', type=str, help='Observation hour', required=True)

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
	obs_site = args.obs_site
	obs_date = args.obs_date
	obs_hour = args.obs_hour

	# Observational site
	#obs_site = 'IMAA_Potenza' # IMAA_Potenza
	# Formato di input: Y,M,D,H,MI,S (MI & S sempre 0)
	#DT = datetime(2018, 9, 24, 10, 0, 0)

	print('***********************')
	print('*** DOD Time Series ***')
	print('***********************')

	print('Observational site: '+obs_site)
	print('Target date: '+obs_date)
	print('Target hour: '+obs_hour)

	# Check implicit basepath
	if args.basepath:
		#data_path = os.path.join(args.basepath, data_path)
		plot_path = os.path.join(args.basepath, plot_path)

	# Check working directory, if any
	#if not os.path.exists(data_path):
	#	os.makedirs(data_path)
	if not os.path.exists(plot_path):
		os.makedirs(plot_path)

	#
	main(obs_site, obs_date, obs_hour)

#
