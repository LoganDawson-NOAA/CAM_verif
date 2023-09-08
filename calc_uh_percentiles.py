#!/usr/bin/env python
import numpy as np
import sys, os, datetime
import shutil
import csv, glob, re
import netCDF4
import dawsonpy


# Get necessary information from environment
try:
    valid = str(sys.argv[1])
except IndexError:
    valid = None

if valid is None:
    valid = os.environ['DATE']


YYYY = int(valid[0:4])
MM = int(valid[4:6])
DD = int(valid[6:8])
HH = int(valid[8:10])

valid_end = datetime.datetime(YYYY,MM,DD,HH,00,00)


# Get machine
machine, hostname = dawsonpy.get_machine()

# Set up working directory
if machine == 'WCOSS':
    pass
elif machine == 'WCOSS_C':
    pass
elif machine == 'WCOSS_DELL_P3':
    system = 'dell'
    SAVE_DIR = '/gpfs/dell2/emc/verification/save/'+os.environ['USER']+'/CAM_verif'
    NOSCRUB_DIR = '/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif'
#   DATA_DIR = NOSCRUB_DIR+'/surrogate_severe/'+valid_end.strftime('%Y%m%d%H')
    THRESH_DIR = NOSCRUB_DIR+'/surrogate_severe/thresholds'

    PTMP_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/CAM_verif/METplus/metplus.out'
    DATA_DIR = PTMP_DIR+'/surrogate_severe/pcp_combine/'+valid_end.strftime('%Y%m%d%H')
#   PTMP_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/UH_accums/'+valid_end.strftime('%Y%m%d%H')

# Make sure threshold directory exists
if not os.path.exists(THRESH_DIR):
    os.makedirs(THRESH_DIR)



hrrr      = []
nam3      = []
hrwarw    = []
hrwarw2   = []
hrwnmmb   = []
hrwfv3    = []
fv3lam    = []
fv3lamx   = []
fv3lamda  = []
fv3lamdax = []

hrrr_fhrs      = []
nam3_fhrs      = []
hrwarw_fhrs    = []
hrwarw2_fhrs   = []
hrwnmmb_fhrs   = []
hrwfv3_fhrs    = []
fv3lam_fhrs    = []
fv3lamx_fhrs   = []
fv3lamda_fhrs  = []
fv3lamdax_fhrs = []

# List of thresholds to calculate
ptiles = [99.85]

# Loop over 24-h max UH native files
filelist = [f for f in glob.glob(DATA_DIR+'/*'+valid+'*.nc')]
for fil in sorted(filelist):

#   filename = fil[88:-3]
    filename = fil[100:-3]

    if str.upper(filename[0:8]) == 'CONUSARW' or str.upper(filename[0:9]) == 'CONUSNMMB' or str.upper(filename[0:8]) == 'CONUSFV3' or str.lower(filename[0:6]) == 'hiresw':
        grid = 'G227'
    elif str.upper(filename[0:6]) == 'FV3LAM':
        grid = 'ESG_CONUS_3km'
    else:
        grid = 'NCEP_3km'

    # Define masking region where percentiles are calculated
    mask_file = NOSCRUB_DIR+'/masks/'+grid+'/CONUS_'+grid+'.nc'
    nc = netCDF4.Dataset(mask_file,'r')
    mask = nc.variables['CONUS'][:]
    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]

    # Mask out values west of 105 deg W 
    # Need to define an appopriate eastern CONUS mask?
    mask[lons < -105.] = 0


    # Open 24-h UH file
    nc = netCDF4.Dataset(fil,'r')
    data = nc.variables['MXUPHL_24'][:]

    # Treat missing values like zeros?
#   data[data < 0.] = 0. 
    # Ignore zeros and missing values
#   data[data <= 0.] = np.nan
    # Ignore missing values
    data[data < 0.] = np.nan 
    # Ignore values outside masking region
    data[mask == 0.] = np.nan

    # Calculate percentiles
    percentiles = np.nanpercentile(data,ptiles)
    print(filename+': ', percentiles)

    # Append forecast hour to end of percentiles list
    fhr = re.findall(re.compile(r"f[0-9]{2}"),fil)
    fhr = str.upper(fhr[0])

    if str.upper(filename[0:4]) == 'HRRR' or str.lower(filename[0:4]) == 'hrrr':
        hrrr.append(percentiles)
        hrrr_fhrs.append(fhr)

    elif str.upper(filename[0:9]) == 'CONUSNEST' or str.lower(filename[0:3]) == 'nam':
        nam3.append(percentiles)
        nam3_fhrs.append(fhr)

    elif str.upper(filename[0:9]) == 'CONUSARW2':
        hrwarw2.append(percentiles)
        hrwarw2_fhrs.append(fhr)

    elif str.upper(filename[0:9]) == 'CONUSARW.':
        hrwarw.append(percentiles)
        hrwarw_fhrs.append(fhr)

    elif str.upper(filename[0:8]) == 'CONUSFV3':
        hrwfv3.append(percentiles)
        hrwfv3_fhrs.append(fhr)

    elif str.upper(filename[0:9]) == 'CONUSNMMB':
        hrwnmmb.append(percentiles)
        hrwnmmb_fhrs.append(fhr)

    elif filename[0:6] == 'hiresw':
 
        if filename[21:24] == 'arw':
            if filename[38:42] == 'mem2':
                hrwarw2.append(percentiles)
                hrwarw2_fhrs.append(fhr)
            else:
                hrwarw.append(percentiles)
                hrwarw_fhrs.append(fhr)

        elif filename[21:24] == 'fv3':
            hrwfv3.append(percentiles)
            hrwfv3_fhrs.append(fhr)

        elif filename[21:25] == 'nmmb':
            hrwnmmb.append(percentiles)
            hrwnmmb_fhrs.append(fhr)

    elif str.lower(filename[0:7]) == 'fv3lam.':
        fv3lam.append(percentiles)
        fv3lam_fhrs.append(fhr)

    elif str.lower(filename[0:8]) == 'fv3lamx.':
        fv3lamx.append(percentiles)
        fv3lamx_fhrs.append(fhr)

    elif str.lower(filename[0:9]) == 'fv3lamda.':
        fv3lamda.append(percentiles)
        fv3lamda_fhrs.append(fhr)

    elif str.lower(filename[0:10]) == 'fv3lamdax.':
        fv3lamdax.append(percentiles)
        fv3lamdax_fhrs.append(fhr)

    else:
        print('something messed up')


#print(np.shape(hrrr))
#print(np.shape(nam3))
#print(np.shape(hrwarw))
#print(np.shape(hrwarw2))
#print(np.shape(hrwfv3))
print(np.shape(hrwnmmb))

# Write percentile values to text files for later use

models = ['hrrr','nam3','hiresw-arw','hiresw-arw2','hiresw-fv3','hiresw-nmmb','fv3lam','fv3lamx','fv3lamda','fv3lamdax']
values = [hrrr,nam3,hrwarw,hrwarw2,hrwfv3,hrwnmmb,fv3lam,fv3lamx,fv3lamda,fv3lamdax]
fhrs   = [hrrr_fhrs,nam3_fhrs,hrwarw_fhrs,hrwarw2_fhrs,hrwfv3_fhrs,hrwnmmb_fhrs,fv3lam_fhrs,fv3lamx_fhrs,fv3lamda_fhrs,fv3lamdax_fhrs]

for model in models:

    model_list = values[models.index(model)]

    # Only try to write percentile data if data exist
    # for current model and the specified valid time
    if model_list:

        # Loop over percentiles of interest
        for ptile in ptiles:

            fhr_list   = fhrs[models.index(model)]
            ptile_str = str(ptile).replace(".","p") 

            thresh_file = THRESH_DIR+'/'+str.lower(model)+'_'+valid_end.strftime('%Y')+'_'+ptile_str+'th_ptile_native.csv'


            # Read any existing data for each model/ptile combination for given year 
            try:
                with open(thresh_file,'r') as f:
                    contents = f.read()
            except:
                contents = ''

            # Append data to file for each model/ptile combination for given year 
            with open(thresh_file,'a+') as f:
                writer = csv.writer(f)
            
                for i in range(len(model_list)):
                    substring = valid[0:4]+','+valid[4:6]+','+valid[6:8]+','+valid[8:10]+','+fhr_list[i]

                    # Only append new data that aren't currently in the file
                    if substring not in contents:
                        writer.writerow([valid[0:4],valid[4:6],valid[6:8],valid[8:10],fhr_list[i],model_list[i][ptiles.index(ptile)]])

