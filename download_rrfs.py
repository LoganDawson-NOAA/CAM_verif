import sys, os, shutil, subprocess
import datetime
import dawsonpy


# Function to write HPSS archive job scripts
def write_download_job(job_script):

    if os.path.exists(job_script):
        os.system('rm -f '+job_script)

    with open(job_script,'w') as f:
        f.write("#!/bin/bash\n")
        f.write("#BSUB -J rrfs_"+mem_num+"\n")
        f.write("#BSUB -o "+OUTPUT_DIR+"/rrfs_"+mem_num+".%J.out\n")
        f.write("#BSUB -e "+OUTPUT_DIR+"/rrfs_"+mem_num+".%J.out\n")
        f.write("#BSUB -n 1\n")
        f.write("#BSUB -W 01:10\n")
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

        f.write("\n")
        f.write("cd "+DATA_DIR+"\n")
        f.write("\n")
        f.write("fhr=0\n")
        f.write("while [ $fhr -le 60 ]; do\n")
        f.write("\n")
        f.write("   FFF=$(printf \"%03d\" ${fhr})\n")
        f.write("\n")
        f.write("   filename=\"rrfs.t"+cyc+"z."+mem_num+".naf${FFF}.grib2\"\n")
        f.write("   wget "+AWS_HEAD+"/"+mem_num+"/${filename}\n")
        f.write("\n")
        f.write("   fhr=$(($fhr+1))\n")
        f.write("\n")
        f.write("done\n")
        f.write("\n")
        f.write("exit\n")
       
        f.close()



# Include option to define valid time on command line
# Used to backfill archive
try:
    cycle = str(sys.argv[1])

    YYYY = int(cycle[0:4])
    MM   = int(cycle[4:6])
    DD   = int(cycle[6:8])
    HH   = int(cycle[8:10])

    init_time = datetime.datetime(YYYY,MM,DD,HH,0,0)
except IndexError:
    init_time = None


# 
if init_time is None:
    current_time = datetime.datetime.utcnow()

    YYYY = int(current_time.strftime('%Y'))
    MM = int(current_time.strftime('%m'))
    DD = int(current_time.strftime('%d'))

    init_time = datetime.datetime(YYYY,MM,DD,0,0,0)


# Define pdy and cyc strings
pdy = init_time.strftime('%Y%m%d')
cyc = init_time.strftime('%H')




try:
    mem_arg = str(sys.argv[2])
    mem_list = [mem_arg]
except IndexError:
    mem_arg = None

if mem_arg is None:
    mem_list = ['01','02','03','04','05','06','07','08','09']


# Get machine
machine, hostname = dawsonpy.get_machine()


# Set up working directory
if machine == 'WCOSS_DELL_P3':
    VERIF_DIR = '/gpfs/dell2/emc/verification/save/'+os.environ['USER']+'/CAM_verif'
    COMROOT = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/com'
    DATA_DIR = os.path.join(COMROOT,'rrfs.'+pdy)
    OUTPUT_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/cron.out'
elif machine == 'WCOSS_C':
    pass

# Create directory where data will be saved
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)



AWS_HEAD = 'https://noaa-rrfs-pds.s3.amazonaws.com/rrfs.'+pdy+'/'+cyc



for mem in mem_list:
    mem_num = 'mem'+mem

    job_script = os.path.join(OUTPUT_DIR,'download_rrfs_'+mem_num+'.sh')
    write_download_job(job_script)
#   dawsonpy.submit_job(job_script)



exit()

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





