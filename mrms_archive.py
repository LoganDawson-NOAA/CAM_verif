import sys, os, shutil, subprocess
import datetime
import re, csv, glob
import bisect
import numpy as np
import dawsonpy


# Function to write HPSS archive job scripts
def write_archive_job(job_script):

    if os.path.exists(job_script):
        os.system('rm -f '+job_script)

    with open(job_script,'w') as f:
        f.write("#!/bin/bash\n")
        f.write("#PBS -N mrms_htar\n")
        f.write("#PBS -o "+OUTPUT_DIR+"/mrms_htar.%J.out\n")
        f.write("#PBS -l select=1:ncpus=1:mem=1000MB\n")
        f.write("#PBS -l walltime=00:10:00\n")
        f.write("#PBS -A VERF-DEV\n")
        f.write("#PBS -q dev_transfer\n")

      # f.write("#PBS -e "+OUTPUT_DIR+"/mrms_htar.%J.out\n")
      # f.write("#BSUB -R \"rusage[mem=1000]\"\n")
      # f.write("#BSUB -R \"affinity[core]\"\n")

        f.write("#\n")
        f.write("set -x\n")
        f.write("\n")

        f.write("source ~/.bashrc\n")

        f.write("\n")
        f.write("cp "+DATA_HEAD+"/"+VALID_DATE+"/* "+ARCH_TEMP+"/\n")
        f.write("cd "+ARCH_TEMP+"\n")
        f.write("\n")
        f.write("gzip ./*\n")
#       if VALID_DATE[-2:] == '03':
        f.write("hsi mkdir -p "+ARCHIVE_DIR+"\n")
        f.write("htar -cvf "+ARCHIVE_DIR+"/"+TAR_FILE+" ./\n")
        f.write("\n")
        f.write("\n")
        f.write("cd .."+"\n")
        f.write("rm -fR "+ARCH_TEMP+"/\n")
        f.write("exit\n")
        f.write("\n")

        f.close()



# Include option to define valid time on command line
# Used to backfill archive
try:
    vday = str(sys.argv[1])

    YYYY = int(vday[0:4])
    MM   = int(vday[4:6])
    DD   = int(vday[6:8])
#   HH   = int(vday[8:10])

    valid = datetime.datetime(YYYY,MM,DD,0,0,0)
except IndexError:
    vday = None

# Zip and archive MRMS files from ptmp
# Done every day on a two-day lag             

# Define valid time to conduct verification 
# Using 24-hr lag 
if vday is None:
    current_time = datetime.datetime.utcnow()
    valid = current_time + datetime.timedelta(hours=-24)


valid_time = valid.strftime('%Y%m%d%H')
VALID_DATE = valid.strftime('%Y%m%d')
print('Zipping and archiving '+VALID_DATE+' MRMS data')


# Get machine
#machine, hostname = dawsonpy.get_machine()


# Set up working directory
VERIF_DIR  = '/lfs/h2/emc/vpppg/save/'+os.environ['USER']+'/CAM_verif'
#DATA_HEAD  = '/lfs/h2/emc/ptmp/'+os.environ['USER']+'/com/MRMS'
DATA_HEAD  = '/lfs/h2/emc/ptmp/'+os.environ['USER']+'/CAM_verif/METplus/metplus.out/regrid/G227/MRMS'
OUTPUT_DIR = '/lfs/h2/emc/ptmp/'+os.environ['USER']+'/cron.out'

# Make sure day's MRMS data exists on ptmp
VALID_DIR = os.path.join(DATA_HEAD,VALID_DATE)
if not os.path.exists(VALID_DIR):
    print("Fatal error: No MRMS data exist for "+valid.strftime('%m/%d/%Y'))
    exit()

# Create temp directory to re-zip files
ARCH_TEMP = os.path.join(DATA_HEAD,'temp')
if not os.path.exists(ARCH_TEMP):
    os.makedirs(ARCH_TEMP)

os.chdir(DATA_HEAD)



# Archive to HPSS
ARCHIVE_DIR = '/NCEPDEV/emc-meso/2year/Logan.Dawson/MRMS/rh'+VALID_DATE[0:4]+'/'+VALID_DATE[0:6]
TAR_FILE = 'MRMS.'+VALID_DATE+'.tar'
job_script = os.path.join(OUTPUT_DIR,'mrms_archive.sh')
write_archive_job(job_script)
dawsonpy.submit_job(job_script)





