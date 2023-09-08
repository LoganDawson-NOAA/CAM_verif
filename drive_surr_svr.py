#!/usr/bin/env python
import numpy as np
import sys, os, datetime
import shutil, time
#import pygrib, netCDF4
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#import mpl_toolkits
#mpl_toolkits.__path__.append('/gpfs/dell3/ptmp/py/lib/python/basemap-1.2.1-py3.6-linux-x86_64.egg/mpl_toolkits/')
#from mpl_toolkits.basemap import Basemap, cm
import dawsonpy



# Function to write scripts to run METplus for each model/field
def write_pcp_job():

    with open(RUN_DIR+'/pcp_'+model+'.sh','w') as f:
        f.write("#!/bin/bash\n")
        f.write("#\n")
        f.write("sleep "+str(wait_time)+"\n")
        f.write(". ~/dots/dot.for.metplus-"+METPLUS_VERSION+"\n")
        f.write("#. ~/dots/dot.for.metplus-test\n")
        f.write("\n")
        f.write("cd "+RUN_DIR+"\n")
        f.write("\n")

        f.write("export ACCUM_BEG="+valid_beg.strftime('%Y%m%d%H')+"\n")
        f.write("export ACCUM_END="+valid_end.strftime('%Y%m%d%H')+"\n")
        f.write("\n")

#       f.write("/gpfs/dell2/emc/verification/save/Logan.Dawson/METplus/ush/master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+
        f.write("master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+
                USE_CASE_DIR+"/"+mxuphl_step1_conf+" "+MODEL_CONF_DIR+"/"+model+".conf\n")

        if model in relv_models:
            f.write("\n")
            f.write("\n")

#           f.write("/gpfs/dell2/emc/verification/save/Logan.Dawson/METplus/ush/master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+
            f.write("master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+
                    USE_CASE_DIR+"/"+relv_step1_conf+" "+MODEL_CONF_DIR+"/"+model+".conf\n")
            f.write("\n")


        f.write("\n")
        f.write("# Copy PcpCombine output to noscrub\n")
        f.write("cp "+METOUT_DIR+"/pcp_combine/"+model+"."+valid_end.strftime('%Y%m%d%H')+"/*.nc "+PCP_DIR+"\n")
        f.write("\n")

        f.write("exit\n")

        f.close()

    os.system('chmod 775 pcp_'+model+'.sh')




# Function to write scripts to run METplus for each model/field
def write_sspf_job():

    with open(RUN_DIR+'/sspf_'+model+'.sh','w') as f:
        f.write("#!/bin/bash\n")
        f.write("#\n")
        f.write("sleep "+str(wait_time)+"\n")
        f.write(". ~/dots/dot.for.metplus-"+METPLUS_VERSION+"\n")
        f.write("#. ~/dots/dot.for.metplus-test\n")
        f.write("\n")
        f.write("cd "+RUN_DIR+"\n")
        f.write("\n")

        f.write("export ACCUM_BEG="+valid_beg.strftime('%Y%m%d%H')+"\n")
        f.write("export ACCUM_END="+valid_end.strftime('%Y%m%d%H')+"\n")
        f.write("\n")

        f.write("export MXUPHL25_THRESH1="+str(uh25_thresh[0])+"\n")
        f.write("export MXUPHL25_THRESH2="+str(uh25_thresh[1])+"\n")
        f.write("export MXUPHL25_THRESH3="+str(uh25_thresh[2])+"\n")
        f.write("\n")

        f.write("export MXUPHL03_THRESH1="+str(uh03_thresh[0])+"\n")
        f.write("export MXUPHL03_THRESH2="+str(uh03_thresh[1])+"\n")
        f.write("export MXUPHL03_THRESH3="+str(uh03_thresh[2])+"\n")
        f.write("\n")

        f.write("export MXUPHL02_THRESH1="+str(uh02_thresh[0])+"\n")
        f.write("export MXUPHL02_THRESH2="+str(uh02_thresh[1])+"\n")
        f.write("export MXUPHL02_THRESH3="+str(uh02_thresh[2])+"\n")
        f.write("\n")

#       f.write("/gpfs/dell2/emc/verification/save/Logan.Dawson/METplus/ush/master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+
        f.write("master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+
                USE_CASE_DIR+"/"+mxuphl_step2_conf+" "+MODEL_CONF_DIR+"/"+model+".conf\n")

        if model in relv_models:
            f.write("\n")
            f.write("\n")
            f.write("export RELV02_THRESH1="+str(vv02_thresh[0])+"\n")
            f.write("export RELV02_THRESH2="+str(vv02_thresh[1])+"\n")
            f.write("export RELV02_THRESH3="+str(vv02_thresh[2])+"\n")
            f.write("\n")

            f.write("export RELV01_THRESH1="+str(vv01_thresh[0])+"\n")
            f.write("export RELV01_THRESH2="+str(vv01_thresh[1])+"\n")
            f.write("export RELV01_THRESH3="+str(vv01_thresh[2])+"\n")
            f.write("\n")

#           f.write("/gpfs/dell2/emc/verification/save/Logan.Dawson/METplus/ush/master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+
            f.write("master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+
                    USE_CASE_DIR+"/"+relv_step2_conf+" "+MODEL_CONF_DIR+"/"+model+".conf\n")
            f.write("\n")


        f.write("\n")
        f.write("# Copy EnsembleStat output to noscrub\n")
        f.write("cp "+METOUT_DIR+"/sspf/"+model+"."+valid_end.strftime('%Y%m%d%H')+"/*.nc "+SSPF_DIR+"\n")
        f.write("\n")

        f.write("echo plotting output\n")
        f.write("\n")
        f.write("python "+SAVE_DIR+"/plotting/sspf_plot.py "+valid_end.strftime('%Y%m%d%H')+" "+model+"\n")
        f.write("\n")

        f.write("exit\n")

        f.close()

    os.system('chmod 775 sspf_'+model+'.sh')


# Function to write job script that regrids 24-h ensemble max
def write_batch_job(jobscript):

    print("Writing SSPF generation script")

    queue = 'dev_shared'
    proj = 'HRW'
    wallclock = '01:00'
    nodes = '96'

    with open(jobscript,'w') as f:
        f.write("#!/bin/bash\n")
        f.write("#BSUB -J surr_svr\n")
        f.write("#BSUB -o "+RUN_DIR+"/"+"surr_svr.out\n")
        f.write("#BSUB -e "+RUN_DIR+"/"+"surr_svr.err\n")
        f.write("#BSUB -W "+wallclock+"\n")
        f.write("#BSUB -n "+nodes+"\n")
        f.write("#BSUB -R span[ptile=16]\n")
        f.write("#BSUB -P "+proj+"-T2O\n")
        f.write("#BSUB -q \""+queue+"\"\n")
        f.write("#BSUB -R \"affinity[core]\"\n")
        f.write("#BSUB -R \"rusage[mem=1500]\"\n")
        f.write("#\n")
        f.write("set +x\n")
        f.write(". ~/dots/dot.for.metplus-"+METPLUS_VERSION+"\n")
        f.write("#. ~/dots/dot.for.metplus-test\n")
        f.write("\n")

        if machine == 'WCOSS':
            f.write("module load lsf\n")
            f.write("module load ibmpe\n")
        elif machine == 'WCOSS_DELL_P3':
            f.write("module load lsf/10.1\n")
            f.write("module load impi/18.0.1\n")
            f.write("module load CFP/2.0.1\n")

        f.write("\n")
        f.write("set -x\n")
        f.write("\n")

        f.write("\n")
        f.write("echo creating directories on noscrub\n")
        f.write("mkdir -p "+PCP_DIR+"\n")
        f.write("mkdir -p "+SSPF_DIR+"\n")
        f.write("\n")

        # Write MPI run for PcpCombine
        if run_pcp_combine:
            poescript = 'poescript1'

            f.write("\n")
            f.write("echo calculating 24-h max fields\n")
            for model in models:
                f.write("echo \""+RUN_DIR+"/pcp_"+model+".sh\" >> "+poescript+"\n")
            f.write("\n")
            f.write("\n")
            f.write("chmod 775 "+poescript+"\n")
            f.write("export MP_PGMMODEL=mpmd\n")
            f.write("export MP_CMDFILE="+poescript+"\n")
            f.write("\n")
            f.write("echo beforelsf1\n")

            if machine == 'WCOSS':
                f.write("mpirun.lsf "+poescript+"\n")
            elif machine == 'WCOSS_DELL_P3':
                pass
                f.write("mpirun -l cfp "+poescript+"\n")

            f.write("echo afterlsf1\n")
            f.write("\n")

            poescript = 'poescript2'

        else:
            poescript = 'poescript'


        # Write MPI run for SSPFs
        f.write("\n")
        f.write("echo calculating deterministic SSPFs\n")
        for model in models:
            f.write("echo \""+RUN_DIR+"/sspf_"+model+".sh\" >> "+poescript+"\n")
        f.write("\n")
        f.write("\n")
        f.write("chmod 775 "+poescript+"\n")
        f.write("export MP_PGMMODEL=mpmd\n")
        f.write("export MP_CMDFILE="+poescript+"\n")
        f.write("\n")
        f.write("echo beforelsf2\n")

        if machine == 'WCOSS':
            f.write("mpirun.lsf "+poescript+"\n")
        elif machine == 'WCOSS_DELL_P3':
            pass
            f.write("mpirun -l cfp "+poescript+"\n")

        f.write("echo afterlsf2\n")
        f.write("\n")

        f.write("\n")
        f.write("echo calculating HREF SSPF/NMEP\n")

        f.write("export ACCUM_BEG="+valid_beg.strftime('%Y%m%d%H')+"\n")
        f.write("export ACCUM_END="+valid_end.strftime('%Y%m%d%H')+"\n")
#       f.write("export INIT_BEG="+init_beg.strftime('%Y%m%d%H')+"\n")
#       f.write("export INIT_END="+init_end.strftime('%Y%m%d%H')+"\n")
        f.write("\n")

        f.write("master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/"+href_conf+" "+MODEL_CONF_DIR+"/CONUSHREF.conf\n")
#       f.write("master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/"+href_conf+" "+MODEL_CONF_DIR+"/CONUSHREFX.conf\n")
#       f.write("/gpfs/dell2/emc/verification/save/Logan.Dawson/METplus/ush/master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/"+href_conf+" "+MODEL_CONF_DIR+"/CONUSHREF.conf\n")
#       f.write("/gpfs/dell2/emc/verification/save/Logan.Dawson/METplus/ush/master_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/"+href_conf+" "+MODEL_CONF_DIR+"/CONUSHREFX.conf\n")

        f.write("\n")
        f.write("# Copy EnsembleStat output to noscrub\n")
        f.write("cp "+METOUT_DIR+"/pcp_combine/CONUSHREF*"+valid_end.strftime('%Y%m%d%H')+"/*.nc "+PCP_DIR+"\n")
        f.write("cp "+METOUT_DIR+"/sspf/CONUSHREF*"+valid_end.strftime('%Y%m%d%H')+"/*.nc "+SSPF_DIR+"\n")
        f.write("\n")

        f.write("\n")
        f.write("echo plotting output\n")
        f.write("python "+SAVE_DIR+"/plotting/sspf_plot.py "+valid_end.strftime('%Y%m%d%H')+" CONUSHREF\n")
#       f.write("python "+SAVE_DIR+"/plotting/sspf_plot.py "+valid_end.strftime('%Y%m%d%H')+" CONUSHREFX\n")
        f.write("\n")

        f.write("echo transfer images to rzdm\n")
        f.write("#bsub < /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/plotting/ftp_surrsvr.sh\n")
        f.write("exit\n")
        f.write("\n")
        f.close()



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

# Get valid end from command line or environment
# Set valid begin as 24 hours prior 
valid_end = datetime.datetime(YYYY,MM,DD,HH,00,00)
valid_beg = valid_end + datetime.timedelta(hours=-24)

# Define HREF inits to compute NMEP
#init_end = valid_beg
#init_beg = valid_beg + datetime.timedelta(hours=-24)


# Determine if PcpCombine needs to be run
# Helpful for regenerating SSPFs with new thresholds, etc.
try:
    rerun = str(sys.argv[2])
except IndexError:
   rerun = None


if rerun is None:
    run_pcp_combine = True
    print('Will run PcpCombine on hourly model output before running EnsembleStat')
else:
    run_pcp_combine = False
    print('Will only run EnsembleStat. PcpCombine accumulations already generated and saved on noscrub.')


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
    PCP_DIR = NOSCRUB_DIR+'/surrogate_severe/pcp_combine/'+valid_end.strftime('%Y%m%d%H')
    SSPF_DIR = NOSCRUB_DIR+'/surrogate_severe/sspf/'+valid_end.strftime('%Y%m%d%H')
    PTMP_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/CAM_verif/METplus'
    METOUT_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/CAM_verif/METplus/metplus.out/surrogate_severe'

if not os.path.exists(PTMP_DIR):
    os.makedirs(PTMP_DIR)


# METplus version (needed for path to conf files)
METPLUS_VERSION = '4.0.0'

# Path to directory where system conf file lives
METPLUS_CONFIG_DIR = os.path.join(SAVE_DIR,'parm','metplus_config','METplus-'+METPLUS_VERSION)

# Path to directory where use case files live
use_case = 'surrogate_severe'
USE_CASE_DIR = os.path.join(SAVE_DIR,'parm','use_cases','METplus-'+METPLUS_VERSION,use_case)

# Use case filenames
mxuphl_step1_conf = 'PcpCombine_fcstCAM_MXUPHL_SurrogateSevere.conf' 
relv_step1_conf   = 'PcpCombine_fcstCAM_RELV_SurrogateSevere.conf' 
mxuphl_step2_conf = 'EnsembleStat_fcstCAM_MXUPHL_SurrogateSevere.conf' 
relv_step2_conf   = 'EnsembleStat_fcstCAM_RELV_SurrogateSevere.conf' 
href_conf         = 'EnsembleStat_fcstHREF_NMEP_SurrogateSevere.conf'

# Path to directory where model conf files live
MODEL_CONF_DIR = os.path.join(SAVE_DIR,'parm','use_cases','METplus-'+METPLUS_VERSION,'model_configs')

# Path to directory to write job scripts
RUN_DIR = os.path.join(PTMP_DIR,'runscripts',use_case,'sspf',valid_end.strftime('%Y%m%d%H'))
if os.path.exists(RUN_DIR):
    shutil.rmtree(RUN_DIR)
os.makedirs(RUN_DIR)
os.chdir(RUN_DIR)


#models = ['CONUSARW','CONUSARW2','CONUSFV3''CONUSNEST','CONUSNMMB','FV3LAM','FV3LAMDA','FV3LAMDAX','FV3LAMX','FV3SAR','FV3SARDA','FV3SARX','HRRR','HRRRX']
models = ['CONUSARW','CONUSARW2','CONUSFV3','CONUSNEST','RRFS_A','FV3LAMDA','FV3LAMDAX','HRRR']

relv_models = ['RRFS_A','FV3LAM','FV3LAMDA','FV3LAMDAX','FV3LAMX','HRRR']

arw_models = ['CONUSARW','CONUSARW2','HRRR']
fv3_models = ['CONUSFV3','FV3LAM','FV3LAMDA','FV3LAMDAX','FV3LAMX','RRFS_A']
nmmb_models = ['CONUSNEST','CONUSNMMB']

# 99.85th percentile thresholds from 2018 HWT
arw_uh25_thresh  = 75.0
fv3_uh25_thresh  = 160.0
nmmb_uh25_thresh = 100.0

# 99.85th percentile thresholds for winter severe
hslc_uh25_thresh = 25.0
hslc_uh03_thresh = 25.0
hslc_uh02_thresh = 25.0
 
# 99.85th percentile thresholds for moving 60-day window 
moving_uh25_thresh = 50.0
moving_uh03_thresh = 50.0
moving_uh02_thresh = 50.0
 

# Loop through models for each use case
wait_time = 0
for model in models:

    # Set HWT threshold based on dynamical coare
    if model in arw_models:
        hwt_uh25_thresh = arw_uh25_thresh
        hwt_uh03_thresh = arw_uh25_thresh
        hwt_uh02_thresh = arw_uh25_thresh
    elif model in fv3_models:
        hwt_uh25_thresh = fv3_uh25_thresh
        hwt_uh03_thresh = fv3_uh25_thresh
        hwt_uh02_thresh = fv3_uh25_thresh
    elif model in nmmb_models:
        hwt_uh25_thresh = nmmb_uh25_thresh
        hwt_uh03_thresh = nmmb_uh25_thresh
        hwt_uh02_thresh = nmmb_uh25_thresh

    uh25_thresh = [hwt_uh25_thresh, hslc_uh25_thresh, moving_uh25_thresh]
    uh03_thresh = [hwt_uh03_thresh, hslc_uh03_thresh, moving_uh03_thresh]
    uh02_thresh = [hwt_uh02_thresh, hslc_uh02_thresh, moving_uh02_thresh]
    
#   vv02_thresh = [hwt_vv02_thresh, hslc_vv02_thresh, moving_uh02_thresh]
#   vv01_thresh = [hwt_vv01_thresh, hslc_vv01_thresh, moving_uh02_thresh]

    vv02_thresh = [round(x*0.0001,4) for x in uh25_thresh]
    vv01_thresh = vv02_thresh

    # Write scripts to run METplus for each model
    if run_pcp_combine:
        write_pcp_job()

    # Write scripts to run METplus for each model
    write_sspf_job()

    # sleep after job submission to help separate METplus log files
    wait_time += 10


# Write and submit batch jobs
job_script = os.path.join(RUN_DIR,'gen_SSPF.sh')
write_batch_job(job_script)
dawsonpy.submit_job(job_script)
#time.sleep(10)


exit()






