#!/usr/bin/env python
# Author: L Dawson
#
# Script to pull fcst files from HPSS, rename, and save in desired data directory
# Desired cycle and model string can be passed in from command line
# If no arguments are passed in, script will prompt user for these inputs
#
# Script History Log:
# 2019-04-11 L Dawson  initial versioning to save HiResW files that are not archived

import numpy as np
import datetime, time, os, sys, subprocess




# Determine initial date/time
try:
   cycle = str(sys.argv[1])
except IndexError:
   cycle = None

if cycle is None:
   cycle = raw_input('Enter model initialization time (YYYYMMDDHH): ')

yyyy = int(cycle[0:4])
mm   = int(cycle[4:6])
dd   = int(cycle[6:8])
hh   = int(cycle[8:10])

date_str = datetime.datetime(yyyy,mm,dd,hh,0,0)
YYYYMMDD_CC = date_str.strftime("%Y%m%d_%H")


# Determine desired model
try:
   model_str = str(sys.argv[2])
except IndexError:
   model_str = None

if model_str is None:
   print('Model string options: HIRESW, HIRESWARW, HIRESWARW2, or HIRESWNMMB')
   model_str = raw_input('Enter desired model: ')



PROD_PATH = '/gpfs/hps/nco/ops/com/hiresw/prod/hiresw.'+cycle[0:8]+'/'
PARA_PATH = '/gpfs/hps2/ptmp/Matthew.Pyle/hiresw/com/hiresw/para/hiresw.'+cycle[0:8]+'/'
#TAR_SUFFIX = '.5km.tar'

if len(model_str) == 6:
   hiresw_member = raw_input('Enter ARW, ARW2, FV3, or NMMB for desired HiResW run: ')
   model_str = model_str+hiresw_member

if str.upper(model_str[6:9]) == 'ARW':
   FILE_PREFIX  = 'hiresw.t'+cycle[8:10]+'z.arw_5km.f'
   FILE_PREFIX2 = 'hiresw.'+cycle[0:8]+'.t'+cycle[8:10]+'z.arw_5km.f'
elif str.upper(model_str[6:]) == 'FV3':
   FILE_PREFIX  = 'hiresw.t'+cycle[8:10]+'z.fv3_5km.f'
   FILE_PREFIX2 = 'hiresw.'+cycle[0:8]+'.t'+cycle[8:10]+'z.fv3_5km.f'
elif str.upper(model_str[6:]) == 'NMMB':
   FILE_PREFIX  = 'hiresw.t'+cycle[8:10]+'z.nmmb_5km.f'
   FILE_PREFIX2 = 'hiresw.'+cycle[0:8]+'.t'+cycle[8:10]+'z.nmmb_5km.f'

if str.upper(model_str[6:]) == 'ARW2':
   FILE_SUFFIX  = '.conusmem2.grib2'
else:
   FILE_SUFFIX  = '.conus.grib2'


# Create data directory (if not already created)
DIR = '/gpfs/hps2/ptmp/Logan.Dawson/com/hiresw/prod'
DATA_DIR = os.path.join(DIR, 'hiresw.'+date_str.strftime('%Y%m%d'))
if not os.path.exists(DATA_DIR):
   os.makedirs(DATA_DIR)
os.chdir(DATA_DIR)



### By default, will ask for command line input to determine which analysis files to pull 
### User can uncomment and modify the next line to bypass the command line calls

if str.upper(model_str[6:]) == 'FV3':
   runlength = 60
else:
   runlength = 48

fhrs = np.arange(0,runlength+1,1)

try:
   fhrs
except NameError:
   fhrs = None

if fhrs is None:
   fhrb = int(raw_input('Enter first forecast hour (cannot be < 0): '))
   if model_str[0:4] == 'HREF' and fhrb == 0:
      fhrb = 1
      print('No 0-h HREF forecast. First forecast hour set to 1')

   fhre = int(raw_input('Enter last forecast hour: '))
   if fhre > runlength:
      fhre = runlength
      print('Invalid run length. Last forecast hour set to '+str(fhre))

   step = int(raw_input('Enter hourly step: '))
   if str.upper(model_str[0:4]) == 'GEFS' and step%6 != 0:
      raise ValueError('Invalid GEFS step')

   fhrs = np.arange(fhrb,fhre+1,step)


print('Array of hours is: ')
print(fhrs)


date_list = [date_str + datetime.timedelta(hours=int(x)) for x in fhrs]


# Loop through
for nf in range(len(date_list)):

   print("Getting "+str(fhrs[nf])+"-h forecast from "+cycle+" "+model_str+" cycle")

   os.system('cp '+PROD_PATH+FILE_PREFIX+str(fhrs[nf]).zfill(2)+FILE_SUFFIX+' '+DATA_DIR+'/'+FILE_PREFIX+str(fhrs[nf]).zfill(2)+FILE_SUFFIX)


print("Done")
