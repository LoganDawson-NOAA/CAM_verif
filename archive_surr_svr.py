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
        f.write("#BSUB -J mrms_htar\n")
        f.write("#BSUB -o "+OUTPUT_DIR+"/"+product+"_htar.%J.out\n")
        f.write("#BSUB -e "+OUTPUT_DIR+"/"+product+"_htar.%J.out\n")
        f.write("#BSUB -n 1\n")
        f.write("#BSUB -W 00:10\n")
        f.write("#BSUB -P HRRR-T2O\n")

        if str.upper(machine) == 'WCOSS':
            f.write("#BSUB -q transfer\n")
        elif str.upper(machine) == 'WCOSS_DELL_P3':
            f.write("#BSUB -q dev_transfer\n")

        f.write("#BSUB -R \"rusage[mem=1000]\"\n")
        f.write("#BSUB -R \"affinity[core]\"\n")
        f.write("#\n")
        f.write("set -x\n")
        f.write("\n")

        if str.upper(machine) == 'WCOSS':
            f.write("module load hpss\n")
        elif str.upper(machine) == 'WCOSS_DELL_P3':
            f.write("module load HPSS/5.0.2.5\n")

        f.write("\n")
        f.write("cp "+DATA_DIR+"/* "+ARCH_TEMP+"/\n")
        f.write("cd "+ARCH_TEMP+"\n")
        f.write("\n")
        f.write("gzip ./*.nc\n")
        f.write("hsi mkdir -p "+ARCHIVE_DIR+"\n")
        f.write("htar -cvf "+ARCHIVE_DIR+"/"+TAR_FILE+" ./\n")
        f.write("\n")
        f.write("\n")
        f.write("cd .."+"\n")
      # f.write("rm -fR "+ARCH_TEMP+"/\n")
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
    HH   = int(vday[8:10])

    valid = datetime.datetime(YYYY,MM,DD,HH,0,0)
except IndexError:
   vday = None

# Zip and archive MRMS files from ptmp
# Done every day on a two-day lag             

# Define valid time to conduct verification 
# Using 24-hr lag 
if vday is None:
    current_time = datetime.datetime.utcnow()
    valid = current_time + datetime.timedelta(hours=-24)


VALID_DATETIME = valid.strftime('%Y%m%d%H')
print('Zipping and archiving '+VALID_DATETIME+' surrogate severe data')


# Get machine
machine, hostname = dawsonpy.get_machine()


# Set up working directory
if machine == 'WCOSS':
    VERIF_DIR = '/gpfs/'+hostname[0]+'d1/emc/meso/save/'+os.environ['USER']+'/CAM_verif'
    DATA_HEAD = '/gpfs/'+hostname[0]+'p2/ptmp/'+os.environ['USER']+'/com/MRMS'
    OUTPUT_DIR = '/gpfs/'+hostname[0]+'p2/ptmp/'+os.environ['USER']+'/cron.out'
elif machine == 'WCOSS_C':
    pass
elif machine == 'WCOSS_DELL_P3':
    VERIF_DIR = '/gpfs/dell2/emc/verification/save/'+os.environ['USER']+'/CAM_verif'
    DATA_HEAD = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/CAM_verif/METplus/metplus.out/surrogate_severe'
    TEMP_HEAD = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/com/surrogate_severe'
    OUTPUT_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/cron.out'



products = ['MXUPHL25_A24','SSPF_MXUPHL25_A24']
for product in products: 

    # 
    if product[0:4] == 'SSPF':
        sub_dir = 'sspf'
    else:
        sub_dir = 'pcp_combine'

    # Directory where METplus output exists
    DATA_DIR = DATA_HEAD+'/'+sub_dir+'/'+VALID_DATETIME

    # If METplus output doesn't exist for current date
    # Skip archivinig process
    if not os.path.exists(DATA_DIR):
        print("No "+product+" data exist for "+valid.strftime('%m/%d/%Y'))
        continue

    # Create temp directory to zip files before archiving
    ARCH_TEMP = TEMP_HEAD+'/'+sub_dir+'/'+VALID_DATETIME
    if not os.path.exists(ARCH_TEMP):
        os.makedirs(ARCH_TEMP)

    os.chdir(ARCH_TEMP)


    # Archive to HPSS
    ARCHIVE_DIR = '/NCEPDEV/emc-meso/2year/Logan.Dawson/surrogate_severe/rh'+ \
                  VALID_DATETIME[0:4]+'/'+VALID_DATETIME[0:6]+'/'+VALID_DATETIME[0:8]
    TAR_FILE = product+'.'+VALID_DATETIME+'.tar'
    job_script = os.path.join(OUTPUT_DIR,'archive_'+str.lower(product)+'.sh')
    write_archive_job(job_script)
    dawsonpy.submit_job(job_script)


#/gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/metplus.out/surrogate_severe/pcp_combine/2021012712
#/gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/metplus.out/surrogate_severe/sspf/2021012712
#/NCEPDEV/emc-meso/2year/Logan.Dawson/surrogate_severe/rh2021/202101/20210127/

#MXUPHL25_A24h.2021012712.tar
#SSPF_MXUPHL25_A24h.2021012712.tar



