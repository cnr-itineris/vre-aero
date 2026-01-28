#!/usr/bin/python3
#
"""
Created on Thu Oct 28 15:45:20 2021

@author: nikolaos.papagiannopoulos@cnr.it
@revision: emilio.lapenna@cnr.it
"""
#
#
import os
import sys
import yaml
#import time
import glob
import numpy as np
import xarray as xr
#
from _plot_module import *

#
code_path = './opprofiles/'
tmp_data_path = './opprofiles/data/tmp/'
output_data_path = './opprofiles/data/'
plot_save_folder = './opprofiles/graphs/'


# Suppress warnings for log function
np.seterr(invalid='ignore')

# Calculate the start_time of the processing
#start = time.time()

#------------------------------------------------------------------------------
# INTRODUCE DATA FROM CONFIGURE FILE
#------------------------------------------------------------------------------
with open(code_path+'cnt_plot.yaml', 'r') as file:
	ct_list = yaml.load(file, Loader=yaml.FullLoader)


#------------------------------------------------------------------------------
# SWITCH CASE
#------------------------------------------------------------------------------

# Define a class "switch"
# https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
class switch(object):
	def __init__(self, value):
		self.value = value
		self.fall = False

	def __iter__(self):
		"""Return the match method once, then stop"""
		yield self.match
		raise StopIteration

	def match(self, *args):
		"""Indicate whether or not to enter a case suite"""
		if self.fall or not args:
			return True
		elif self.value in args: # changed for v1.5, see below
			self.fall = True
			return True
		else:
			return False


def make_range_consistent(range1, range2, data1, data1_e, data2, data2_e):
	'''
	Parameters
	----------
	range1 : ndarray
		The range of data1.
	range2 : ndarray
		The range of data2.
	data1 : ndarray
	data2 : ndarray
	data1_e : ndarray
	data2_e : ndarray

	Returns
	-------
	Consistent with range data1 and data2
	'''
	# Find the min and max for consistent estimation
	min_height = np.maximum(range1[0],range2[0])
	max_height = np.minimum(range1[-1],range2[-1])
	# The range for plotting
	range1_step1 = range1[range1>=min_height]
	range1_step2 = range1_step1[range1_step1<=max_height]
	range2_step1 = range2[range2>=min_height]
	#range2_step2 = range2_step1[range2_step1<=max_height]
	#
	data1 = data1[0,0,:]
	data1_RD = data1[range1>=min_height]
	data1_RD = data1_RD[range1_step1<=max_height]
	data1_e = data1_e[0,0,:]
	data1_e_RD = data1_e[range1>=min_height]
	data1_e_RD = data1_e_RD[range1_step1<=max_height]
	#
	data2 = data2[0,0,:]
	data2_RD = data2[range2>=min_height]
	data2_RD = data2_RD[range2_step1<=max_height]
	data2_e = data2_e[0,0,:]
	data2_e_RD = data2_e[range2>=min_height]
	data2_e_RD = data2_e_RD[range2_step1<=max_height]
	#
	return range1_step2, data1_RD, data1_e_RD, data2_RD, data2_e_RD


# elda_DIR = cnfg['tmp_data_path'] # Contains also D355
# B0355 = glob.glob(elda_DIR + "/*_007_0355*" + ".nc", recursive=True)
# DS_elda = xr.open_dataset(B0355[0], decode_times=False)

def main(fromDate, toDate, fromHour, toHour, station, panel, basepath):

	global output_data_path

	#
	#type_v = ct_list['type']

	for case in switch(panel):

		if case('5p'):
			#----------------------------------------------------------------------
			# READ THE DATA
			#----------------------------------------------------------------------
			# The data file
			elda_DIR = output_data_path
			#
			"""
			b0355_DIR = glob.glob(elda_DIR + "/*_007_0355*" + ".nc", recursive=True)
			b0532_DIR = glob.glob(elda_DIR + "/*_007_0532*" + ".nc", recursive=True)
			b1064_DIR = glob.glob(elda_DIR + "/*_008_1064*" + ".nc", recursive=True)
			e0355_DIR = glob.glob(elda_DIR + "/*_002_0355*" + ".nc", recursive=True)
			e0532_DIR = glob.glob(elda_DIR + "/*_002_0532*" + ".nc", recursive=True)
			"""
			#
			b0355_DIR = glob.glob(elda_DIR + "/*_b0355*" + ".nc", recursive=True)
			b0532_DIR = glob.glob(elda_DIR + "/*_b0532*" + ".nc", recursive=True)
			b1064_DIR = glob.glob(elda_DIR + "/*_b1064*" + ".nc", recursive=True)
			e0355_DIR = glob.glob(elda_DIR + "/*_e0355*" + ".nc", recursive=True)
			e0532_DIR = glob.glob(elda_DIR + "/*_e0532*" + ".nc", recursive=True)
			#
			DS_b0355 = xr.open_dataset(b0355_DIR[0], decode_times=False)
			DS_b0532 = xr.open_dataset(b0532_DIR[0], decode_times=False)
			DS_b1064 = xr.open_dataset(b1064_DIR[0], decode_times=False)
			DS_e0355 = xr.open_dataset(e0355_DIR[0], decode_times=False)
			DS_e0532 = xr.open_dataset(e0532_DIR[0], decode_times=False)
			#
			# Parameters: backscatter, error_backscatter
			# Parameters: altitude, vertical_resolution
			# Parameters: particledepolarization, error_particledepolarization
			# Parameters: volumedepolarization, error_volumedepolarization
			# 355
			b0355 = DS_b0355.backscatter.values
			b0355_e = DS_b0355.error_backscatter.values
			d0355 = DS_b0355.particledepolarization.values
			d0355_e = DS_b0355.error_particledepolarization.values
			v0355 = DS_b0355.volumedepolarization.values
			v0355_e = DS_b0355.error_volumedepolarization.values
			height_b0355 = DS_b0355.altitude.values
			VResol_0355 = DS_b0355.vertical_resolution
			# 532
			b0532 = DS_b0532.backscatter.values
			b0532_e = DS_b0532.error_backscatter.values
			d0532 = DS_b0532.particledepolarization.values
			d0532_e = DS_b0532.error_particledepolarization.values
			v0532 = DS_b0532.volumedepolarization.values
			v0532_e = DS_b0532.error_volumedepolarization.values
			height_b0532 = DS_b0532.altitude.values
			VResol_0532 = DS_b0532.vertical_resolution
			# 1064
			b1064 = DS_b1064.backscatter.values
			b1064_e = DS_b1064.error_backscatter.values
			d1064 = DS_b1064.particledepolarization.values
			d1064_e = DS_b1064.error_particledepolarization.values
			v1064 = DS_b1064.volumedepolarization.values
			v1064_e = DS_b1064.error_volumedepolarization.values
			height_b1064 = DS_b1064.altitude.values
			VResol_1064 = DS_b1064.vertical_resolution
			# Raman 355
			e0355 = DS_e0355.extinction.values
			e0355_e = DS_e0355.error_extinction.values
			e0355_bRaman =  DS_e0355.backscatter.values
			e0355_bRaman_e =  DS_e0355.error_backscatter.values
			height_e0355 = DS_e0355.altitude.values
			# Raman 532
			e0532 = DS_e0532.extinction.values
			e0532_e = DS_e0532.error_extinction.values
			e0532_bRaman =  DS_e0532.backscatter.values
			e0532_bRaman_e =  DS_e0532.error_backscatter.values
			height_e0532 = DS_e0532.altitude.values
			#----------------------------------------------------------------------
			# Calculate the intensive parameters
			#----------------------------------------------------------------------
			# Estimate the lidar ratio
			S0355 = e0355/e0355_bRaman; S0355 = S0355[0,0,:]
			S0355_e = S0355 * np.sqrt((e0355_e/e0355)**2 + (e0355_bRaman_e/e0355_bRaman)**2)
			#
			S0532 = e0532/e0532_bRaman; S0532 = S0532[0,0,:]
			S0532_e = S0532 * np.sqrt((e0532_e/e0532)**2 + (e0532_bRaman_e/e0532_bRaman)**2)

			# Estimate the b-Angstrom exponent
			# 532 nm / 1064 nm
			r_532_1064, b0532_RD, b0532_e_RD, b1064_RD, b1064_e_RD = \
				make_range_consistent(height_b0532, height_b1064, b0532, b0532_e, b1064, b1064_e)
			#
			AEb_532_1064 = -np.log(b0532_RD/b1064_RD)/np.log(532.0/1064)
			#AEb_532_1064_e = abs(np.log(532.0/1064)*((b0532_e_RD/b0532_RD)+(b1064_e_RD/b1064_RD)))
			AEb_532_1064_e = np.log(1064/532.)*np.sqrt((b0532_e_RD/b0532_RD)**2 + (b1064_e_RD/b1064_RD)**2)

			# Estimate the b-Angstrom exponent
			# 355 nm / 532 nm
			r_355_532, b0355_RD, b0355_e_RD, b0532_RD, b0532_e_RD = \
				make_range_consistent(height_b0355, height_b0532, b0355, b0355_e, b0532, b0532_e)
			#
			AEb_355_532 = -np.log(b0355_RD/b0532_RD)/np.log(355.0/532)
			#AEb_355_532_e = abs(np.log(355.0/532)*((b0355_e_RD/b0355_RD)+(b0532_e_RD/b0532_RD)))
			AEb_355_532_e = np.log(532/355.)*np.sqrt((b0355_e_RD/b0355_RD)**2 + (b0532_e_RD/b0532_RD)**2)

			# Estimate the b-Angstrom exponent
			# 355 nm / 1064 nm
			r_355_1064, b0355_RD, b0355_e_RD, b1064_RD, b1064_e_RD = \
				make_range_consistent(height_b0355, height_b1064, b0355, b0355_e, b1064, b1064_e)
			#
			AEb_355_1064 = -np.log(b0355_RD/b1064_RD)/np.log(355.0/1064)
			#AEb_355_1064_e = abs(np.log(355.0/1064)*((b0355_e_RD/b0355_RD)+(b1064_e_RD/b1064_RD)))
			AEb_355_1064_e = np.log(1064./355.)*np.sqrt((b0355_e_RD/b0355_RD)**2 + (b1064_e_RD/b1064_RD)**2)

			# Estimate the a-Angstrom exponent
			# 355 nm / 532 nm
			r_a_355_532, e0355_RD, e0355_e_RD, e0532_RD, e0532_e_RD = \
				make_range_consistent(height_e0355, height_e0532, e0355, e0355_e, e0532, e0532_e)
			#
			AEe_355_532 = -np.log(e0355_RD/e0532_RD)/np.log(355.0/532)
			#AEe_355_532_e = abs(np.log(355.0/532)*((e0355_e_RD/e0355_RD)+(e0532_e_RD/e0532_RD)))
			AEe_355_532_e = np.log(532./355.)*np.sqrt((e0355_e_RD/e0355_RD)**2 + (e0532_e_RD/e0532_RD)**2)

			#----------------------------------------------------------------------
			# PLOTTING
			#----------------------------------------------------------------------
			# Retrieve the filename of the elic data
			basename = os.path.basename(station+'_'+fromDate+'_'+fromHour.replace(':','')+'_'+toDate+'_'+toHour.replace(':','')+'_'+panel)
			#print(basename)

			plot_night(b0355,b0355_e,height_b0355,b0532,b0532_e,height_b0532,b1064,b1064_e,height_b1064,
					e0355,e0355_e,height_e0355,e0532,e0532_e,height_e0532,
					AEb_355_1064,AEb_355_1064_e,r_355_1064,
					AEb_355_532,AEb_355_532_e,r_355_532,
					AEb_532_1064,AEb_532_1064_e,r_532_1064,
					AEe_355_532,AEe_355_532_e,r_a_355_532,
					S0355,S0355_e,S0532,S0532_e,
					d0532,d0532_e,v0532,v0532_e,
					d0355,d0355_e,v0355,v0355_e,
					d1064,d1064_e,v1064,v1064_e,
					basename, basepath)
			break

		if case('3p'):
			#----------------------------------------------------------------------
			# READ THE DATA
			#----------------------------------------------------------------------
			# The data file
			elda_DIR = output_data_path
			#
			"""
			b0355_DIR = glob.glob(elda_DIR + "/*_008_0355*" + ".nc", recursive=True)
			b0532_DIR = glob.glob(elda_DIR + "/*_008_0532*" + ".nc", recursive=True)
			b1064_DIR = glob.glob(elda_DIR + "/*_008_1064*" + ".nc", recursive=True)
			"""
			#
			b0355_DIR = glob.glob(elda_DIR + "/*_b0355*" + ".nc", recursive=True)
			b0532_DIR = glob.glob(elda_DIR + "/*_b0532*" + ".nc", recursive=True)
			b1064_DIR = glob.glob(elda_DIR + "/*_b1064*" + ".nc", recursive=True)
			#
			DS_b0355 = xr.open_dataset(b0355_DIR[0], decode_times=False)
			DS_b0532 = xr.open_dataset(b0532_DIR[0], decode_times=False)
			DS_b1064 = xr.open_dataset(b1064_DIR[0], decode_times=False)
			#
			# Parameters: backscatter, error_backscatter
			# Parameters: altitude, vertical_resolution
			# Parameters: particledepolarization, error_particledepolarization
			# Parameters: volumedepolarization, error_volumedepolarization
			# 355
			b0355 = DS_b0355.backscatter.values
			b0355_e = DS_b0355.error_backscatter.values
			d0355 = DS_b0355.particledepolarization.values
			d0355_e = DS_b0355.error_particledepolarization.values
			v0355 = DS_b0355.volumedepolarization.values
			v0355_e = DS_b0355.error_volumedepolarization.values
			height_b0355 = DS_b0355.altitude.values
			VResol_0355 = DS_b0355.vertical_resolution
			# 532
			b0532 = DS_b0532.backscatter.values
			b0532_e = DS_b0532.error_backscatter.values
			d0532 = DS_b0532.particledepolarization.values
			d0532_e = DS_b0532.error_particledepolarization.values
			v0532 = DS_b0532.volumedepolarization.values
			v0532_e = DS_b0532.error_volumedepolarization.values
			height_b0532 = DS_b0532.altitude.values
			VResol_0532 = DS_b0532.vertical_resolution
			# 1064
			b1064 = DS_b1064.backscatter.values
			b1064_e = DS_b1064.error_backscatter.values
			d1064 = DS_b1064.particledepolarization.values
			d1064_e = DS_b1064.error_particledepolarization.values
			v1064 = DS_b1064.volumedepolarization.values
			v1064_e = DS_b1064.error_volumedepolarization.values
			height_b1064 = DS_b1064.altitude.values
			VResol_1064 = DS_b1064.vertical_resolution
			hehe = DS_b1064.cirrus_contamination

			#----------------------------------------------------------------------
			# Calculate the intensive parameters
			#----------------------------------------------------------------------
			# Estimate the b-Angstrom exponent
			# 532 nm / 1064 nm
			r_532_1064, b0532_RD, b0532_e_RD, b1064_RD, b1064_e_RD = \
				make_range_consistent(height_b0532, height_b1064, b0532, b0532_e, b1064, b1064_e)
			#
			AEb_532_1064 = -np.log(b0532_RD/b1064_RD)/np.log(532.0/1064)
			AEb_532_1064_e = abs(np.log(532.0/1064)*((b0532_e_RD/b0532_RD)+(b1064_e_RD/b1064_RD)))

			# Estimate the b-Angstrom exponent
			# 355 nm / 532 nm
			r_355_532, b0355_RD, b0355_e_RD, b0532_RD, b0532_e_RD = \
				make_range_consistent(height_b0355, height_b0532, b0355, b0355_e, b0532, b0532_e)
			#
			AEb_355_532 = -np.log(b0355_RD/b0532_RD)/np.log(355.0/532)
			AEb_355_532_e = abs(np.log(355.0/532)*((b0355_e_RD/b0355_RD)+(b0532_e_RD/b0532_RD)))

			# Estimate the b-Angstrom exponent
			# 355 nm / 1064 nm
			r_355_1064, b0355_RD, b0355_e_RD, b1064_RD, b1064_e_RD = \
				make_range_consistent(height_b0355, height_b1064, b0355, b0355_e, b1064, b1064_e)
			#
			AEb_355_1064 = -np.log(b0355_RD/b1064_RD)/np.log(355.0/1064)
			AEb_355_1064_e = abs(np.log(355.0/1064)*((b0355_e_RD/b0355_RD)+(b1064_e_RD/b1064_RD)))

			#----------------------------------------------------------------------
			# PLOTTING
			#----------------------------------------------------------------------
			# Retrieve the filename of the elic data
			basename = os.path.basename(station+'_'+fromDate+'_'+fromHour.replace(':','')+'_'+toDate+'_'+toHour.replace(':','')+'_'+panel)
			#print(basename)

			plot_day(b0355,b0355_e,height_b0355,b0532,b0532_e,height_b0532,b1064,b1064_e,height_b1064,
					AEb_355_1064,AEb_355_1064_e,r_355_1064,
					AEb_355_532,AEb_355_532_e,r_355_532,
					AEb_532_1064,AEb_532_1064_e,r_532_1064,
					d0532,d0532_e,v0532,v0532_e,
					d0355,d0355_e,v0355,v0355_e,
					d1064,d1064_e,v1064,v1064_e,
					basename, basepath)
			break

		if case(): # default, could also just omit condition or 'if True'
			print('Type is case sensitive!')
			# No need to break here, it'll stop anyway

# Main program
if __name__ == '__main__':
	#
	#print('#############################')
	#print('#     Elda plot routine     #')
	#print('#############################')
	#
	if len(sys.argv) < 7:
		print('ERROR: Please provide enough string arguments (7)!')
	else:
		fromDate = sys.argv[1]
		toDate = sys.argv[2]
		fromHour = sys.argv[3]
		toHour = sys.argv[4]
		station = sys.argv[5]
		panel = sys.argv[6]
		basepath = sys.argv[7]

	main(fromDate, toDate, fromHour, toHour, station, panel, basepath)

# Calculate the end_time of the processing
#end = time.time()
# Print the Processing time of the
#print(end - start)

#