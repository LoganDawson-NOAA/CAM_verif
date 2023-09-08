import sys, os, shutil, subprocess
import datetime
import re, csv, glob
import bisect
import numpy as np
import dawsonpy


# Function to write script to generate extra fields
def write_regrid_job(job_script):

    if os.path.exists(job_script):
        os.system('rm -f '+job_script)


    with open(job_script,'w') as f:
        f.write("#!/bin/bash\n")
        f.write("#BSUB -J regrid_mrms\n")
        f.write("#BSUB -o "+RUN_DIR+"/regrid_mrms.out\n")
        f.write("#BSUB -e "+RUN_DIR+"/regrid_mrms.err\n")
        f.write("#BSUB -W 01:15\n")
        f.write("#BSUB -n 80\n")
        f.write("#BSUB -R span[ptile=16]\n")
        f.write("#BSUB -P HRW-T2O\n")
        f.write("#BSUB -q \"dev_shared\"\n")
        f.write("#BSUB -R \"affinity[core]\"\n")
        f.write("#BSUB -R \"rusage[mem=1500]\"\n")
        f.write("#\n")
        f.write("set +x\n")
        f.write(". ~/dots/dot.for.metplus-"+METPLUS_VERSION+"\n")
    #   f.write("export PYTHONPATH=${PYTHONPATH}:/gpfs/dell2/emc/modeling/noscrub/Jacob.Carley/python/lib:/gpfs/dell2/emc/verification/save/Logan.Dawson/python\n")

        f.write("\n")
        f.write("set -x\n")
        f.write("\n")

        f.write("# Set environment variables needed for METplus job\n")
        f.write("export DATE="+valid_time+"\n")
        f.write("export TOGRID=G227\n")
        f.write("\n")

        f.write("MRMS_PRODUCTS=\"REFC REFD1 RETOP\"\n")
        f.write("\n")
        f.write("# Regrid each MRMS product\n")
        f.write("for MRMS_PRODUCT in ${MRMS_PRODUCTS}; do\n")
        f.write("\n")
        f.write("   echo \"regridding MRMS ${MRMS_PRODUCT} file to ${TOGRID}\"\n")
        f.write("\n")
        f.write("   master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/RegridDataPlane_obsMRMS_${MRMS_PRODUCT}_toG227.conf\n")

        f.write("\n")
        f.write("   echo \"creating 40-km max field for MRMS ${MRMS_PRODUCT}\"\n")
        f.write("\n")
        f.write("   master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/RegridDataPlane_obsMRMS_${MRMS_PRODUCT}_NBMAX.conf\n")
        f.write("\n")
        f.write("done")

        f.write("\n")
        f.write("\n")
        f.write("# Generate binary and observation probability field for all MRMS products\n")
        f.write("python /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/mrms_obs_fields.py\n")
        f.write("\n")
        f.write("\n")

        f.write("# Generate practically perfect forecast fields\n")
        f.write("for MRMS_PRODUCT in ${MRMS_PRODUCTS}; do\n")
        f.write("\n")
        f.write("   echo \"generating MRMS ${MRMS_PRODUCT} practically perfect forecast field\"\n")
        f.write("\n")
        f.write("   master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/RegridDataPlane_obsMRMS_${MRMS_PRODUCT}_PPF.conf\n")
        f.write("\n")
        f.write("done")
        f.write("\n")

        f.write("\n")
        f.write(". "+SAVE_DIR+"/plotting/plot_mrms.sh "+valid_time+"\n")
        f.write("\n")

        f.close()


# Copy and unzip MRMS files that are closest to top of hour
# Done every hour on a 20-minute lag             

# Include option to define valid time on command line
# Used to backfill verification
try:
    valid_time = str(sys.argv[1])

    YYYY = int(valid_time[0:4])
    MM   = int(valid_time[4:6])
    DD   = int(valid_time[6:8])
    HH   = int(valid_time[8:10])

    valid = datetime.datetime(YYYY,MM,DD,HH,0,0)
except IndexError:
   valid_time = None


# Default to 24-hr verification lag if not defined on command line 
# Will adjust time for other use cases, if needed 
if valid_time is None:
    now  = datetime.datetime.utcnow()
    YYYY = int(now.strftime('%Y'))
    MM   = int(now.strftime('%m'))
    DD   = int(now.strftime('%d'))
    HH   = int(now.strftime('%H'))

    valid = datetime.datetime(YYYY,MM,DD,HH,0,0)
    valid_time = valid.strftime('%Y%m%d%H')



print('Copying and unzipping '+valid_time+' MRMS data')




# Get machine
machine, hostname = dawsonpy.get_machine()


# Set up working directory
if machine == 'WCOSS':
    VERIF_DIR = '/gpfs/'+hostname[0]+'d1/emc/meso/save/'+os.environ['USER']+'/CAM_verif'
    DATA_HEAD = '/gpfs/'+hostname[0]+'p2/ptmp/'+os.environ['USER']+'/com/MRMS'
    MRMS_PROD_DIR = '/dcom/us007003/ldmdata/obs/upperair/mrms/conus'
    OUTPUT_DIR = '/gpfs/'+hostname[0]+'p2/ptmp/'+os.environ['USER']+'/cron.out'
elif machine == 'WCOSS_C':
    pass
elif machine == 'WCOSS_DELL_P3':
    system = 'dell'
    SAVE_DIR = '/gpfs/dell2/emc/verification/save/'+os.environ['USER']+'/CAM_verif'
    DATA_HEAD = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/com/MRMS'
    MRMS_PROD_DIR = '/gpfs/dell1/ptmp/Geoffrey.Manikin/mrms/upperair/mrms/conus'
    MRMS_PROD_DIR = '/gpfs/dell2/ptmp/Logan.Dawson/com/MRMS/hold/upperair/mrms/conus'
    RUN_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/CAM_verif/METplus/runscripts/MRMS/'+valid_time


VALID_DIR = os.path.join(DATA_HEAD,valid.strftime('%Y%m%d'))
if not os.path.exists(VALID_DIR):
    os.makedirs(VALID_DIR)
os.chdir(DATA_HEAD)

if not os.path.exists(RUN_DIR):
    os.makedirs(RUN_DIR)


# METplus version (needed for path to conf files)
METPLUS_VERSION = '3.1'

# Path to directory where system conf file lives
METPLUS_CONFIG_DIR = os.path.join(SAVE_DIR,'parm','metplus_config','METplus-'+METPLUS_VERSION)

# Directory where use case conf files live
USE_CASE_DIR = os.path.join(SAVE_DIR,'parm','use_cases','METplus-'+METPLUS_VERSION,'regrid_mrms_obs')


# Copy and unzip the following MRMS products
MRMS_PRODUCTS = ['MergedReflectivityQCComposite','SeamlessHSR','EchoTop']
MRMS_PRODUCTS = ['MergedReflectivityQCComposite']

for MRMS_PRODUCT in MRMS_PRODUCTS:

    if MRMS_PRODUCT == 'MergedReflectivityQCComposite':
        level = '_00.50_'
    elif MRMS_PRODUCT == 'SeamlessHSR':
        level = '_00.00_'
    elif MRMS_PRODUCT == 'EchoTop':
        level = '_18_00.50_'

    # Sort list of files for each MRMS product
    search_path = MRMS_PROD_DIR+'/'+MRMS_PRODUCT+'/'+MRMS_PRODUCT+'*.gz'
    file_list = [f for f in glob.glob(search_path)]
    time_list = [file_list[x][-24:-9] for x in range(len(file_list))]
    int_list = [int(time_list[x][0:8]+time_list[x][9:15]) for x in range(len(time_list))]
    int_list.sort()
    datetime_list = [datetime.datetime.strptime(str(x),"%Y%m%d%H%M%S") for x in int_list]
 
    # Find the MRMS file closest to the valid time
    i = bisect.bisect_left(datetime_list,valid)
    closest_timestamp = min(datetime_list[max(0, i-1): i+2], key=lambda date: abs(valid - date))

    # Check to make sure closest file is within +/- 15 mins of top of the hour
    # Copy and rename the file for future ease
    difference = abs(closest_timestamp - valid)
    if difference.total_seconds() <= 900:
        filename1 = MRMS_PRODUCT+level+closest_timestamp.strftime('%Y%m%d-%H%M%S')+'.grib2.gz'
        filename2 = MRMS_PRODUCT+level+valid.strftime('%Y%m%d-%H')+'0000.grib2.gz'

        os.system('cp '+MRMS_PROD_DIR+'/'+MRMS_PRODUCT+'/'+filename1+' '+VALID_DIR+'/'+filename2)
        os.system('gunzip '+VALID_DIR+'/'+filename2)
    else:
        print('No '+MRMS_PRODUCT+' file found within 15 minutes of '+valid.strftime('%HZ %m/%d/%Y')+'. Skipping this time.')




# Regrid MRMS data to G227
job_script = os.path.join(RUN_DIR,'mrms_regrid.sh')
write_regrid_job(job_script)
dawsonpy.submit_job(job_script)





