import sys
import datetime
import shutil
import os, time 
import subprocess, re, glob
import dawsonpy


# Function to write scripts to run METplus for each model/field
def write_metplus_job():

    if os.path.exists(RUN_DIR+'/verif_'+model+'_'+field+'.sh'):
        os.system('rm -f '+RUN_DIR+'/verif_'+model+'_'+field+'.sh')


    with open(RUN_DIR+'/verif_'+model+'_'+field+'.sh','w') as f:
        f.write("#!/bin/bash\n")
        f.write("#\n")
        f.write("sleep "+str(wait_time)+"\n")
        f.write(". ~/dots/dot.for.metplus-"+METPLUS_VERSION+"\n")
        f.write("\n")
        f.write("cd "+RUN_DIR+"\n")
        f.write("\n")

        f.write("export VDATE="+valid_time.strftime('%Y%m%d%H')+"\n")
        f.write("export MASKS=\""+mask_str+"\"\n")
        f.write("\n")


        # METplus commands for grid2grid_mrms
        if use_case == 'grid2grid_mrms':

            # Probabilistic verification
            if model == 'CONUSHREF_PROB' or model == 'CONUSHREFX_PROB':
                f.write("run_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/GridStat_fcstHREFPROB_obsMRMS_"+str.upper(field)+".conf "+MODEL_CONF_DIR+"/"+model+".conf\n")
                f.write("run_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/GridStat_prob_fcstHREFPROB_obsMRMS_"+str.upper(field)+".conf "+MODEL_CONF_DIR+"/"+model+".conf\n")
            # Deterministic verification
            else:
                f.write("run_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/GridStat_fcstCAM_obsMRMS_"+str.upper(field)+".conf "+MODEL_CONF_DIR+"/"+model+".conf\n")


        # METplus commands for surrogate_severe
        elif use_case == 'surrogate_severe':

            f.write("run_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/GridStat_fcstCAM_SSPF_obsLSR_PPF.conf "+MODEL_CONF_DIR+"/"+model+".conf\n")
            f.write("run_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/GridStat_prob_fcstCAM_SSPF_obsLSR_PPF.conf "+MODEL_CONF_DIR+"/"+model+".conf\n")


        # METplus commands for grid2obs
        elif use_case == 'grid2obs':

            f.write("export PB2NC_GRID="+pb2nc_grid+"\n")
            f.write("\n")
           #f.write("run_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/PB2NC_obsNDAS_PrepBufr.conf "+MODEL_CONF_DIR+"/"+model+".conf\n")
            f.write("run_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/PointStat_fcstCAM_obsNDAS_PrepBufr.conf "+MODEL_CONF_DIR+"/"+model+".conf\n")


        f.write("\n")
        f.write("exit\n")
        f.write("\n")

        f.close()

    os.system('chmod 775 verif_'+model+'_'+field+'.sh')



# Function to write batch script for each model
def write_batch_job(model, fields):

    queue = 'debug'
    queue = 'dev'

    if queue == 'debug':
        wallclock = '00:30:00'
        if str.upper(model[0:4]) == 'HRRR':
            nodes = 80
        elif str.upper(model) == 'CONUSNEST':
            nodes = 64
        else:
            nodes = 64

    elif queue == 'dev':
        if str.upper(model[0:4]) == 'HRRR':
            wallclock = '01:00:00'
            nodes = 144
            ncpus = 128

        elif str.upper(model) == 'CONUSNEST':
            if valid_hour%3 == 0:
                wallclock = '00:30:00'
                nodes = 96
                ncpus = 96
            else:
                wallclock = '00:15:00'
                nodes = 64
                ncpus = 64

        elif str.upper(model[-4:]) == 'MEAN' or str.upper(model[-4:]) == 'PMMN':
            wallclock = '00:45:00'
            nodes = 144
            ncpus = 64

        elif str.upper(model[-4:]) == 'PROB':
            wallclock = '01:00:00'
            nodes = 144
            ncpus = 128

        else:
            if valid_hour%3 == 0:
                wallclock = '00:30:00'
                nodes = 64
                ncpus = 64
            else:
                wallclock = '00:15:00'
                nodes = 64
                ncpus = 32


        if use_case == 'surrogate_severe':
            wallclock = '00:40:00'
            nodes = '16'
 

    ncpus = 16
    wallclock = '00:30:00'

    with open(RUN_DIR+'/verif_'+model+'.sh','w') as f:
        f.write("#!/bin/ksh\n")
        f.write("#\n")
        f.write("#PBS -N verif_"+str.lower(model)+"\n")
        f.write("#PBS -o "+RUN_DIR+"/"+str.lower(model)+".out\n")
        f.write("#PBS -e "+RUN_DIR+"/"+str.lower(model)+".err\n")
        f.write("#PBS -l walltime="+wallclock+"\n")
     #  f.write("#PBS -l select=1:ncpus="+str(nodes/64)+":mem=1GB\n")
        f.write("#PBS -l select=1:ncpus="+str(ncpus)+":ompthreads=1\n")
        f.write("#PBS -A VERF-DEV\n")
        f.write("#PBS -q "+queue+" \n")
        f.write("#PBS -m ae\n")
        f.write("#PBS -WMail_Users="+os.environ['USER']+"@noaa.gov\n")

       #f.write("#BSUB -n "+nodes+"\n")
       #f.write("#BSUB -R span[ptile=16]\n")
        if machine == 'WCOSS':
            f.write("#BSUB -q \"dev2\" \n")
            f.write("#BSUB -R \"affinity[core]\"\n")
            f.write("#BSUB -x\n")
            f.write("#BSUB -a poe\n")
        elif machine == 'WCOSS_DELL_P3':
            f.write("#BSUB -q \""+queue+"\" \n")
            f.write("#BSUB -R \"affinity[core]\"\n")
         #  f.write("#BSUB -R \"affinity[core(4)]\"\n")
            f.write("#BSUB -R \"rusage[mem=1500]\"\n")

        f.write("#\n")
        f.write("set -x\n")
        f.write("\n")
        f.write("cd $PBS_O_WORKDIR\n")
        f.write("\n")
        f.write(". ~/dots/dot.for.metplus-"+METPLUS_VERSION+"\n")
        f.write("\n")

        if machine == 'WCOSS':
            f.write("module load lsf\n")
            f.write("module load ibmpe\n")
        elif machine == 'WCOSS_DELL_P3':
            f.write("module load lsf/10.1\n")
            f.write("module load impi/18.0.1\n")
            f.write("module load CFP/2.0.1\n")




        # Extra environment variables for surrogate_severe use case
        if use_case == 'surrogate_severe':
            f.write("export ACCUM_BEG="+valid_beg.strftime('%Y%m%d%H')+"\n")
            f.write("export ACCUM_END="+valid_end.strftime('%Y%m%d%H')+"\n")
            f.write("export REP_MONTH="+valid_beg.strftime('%Y%m')+"\n")
            f.write("\n")

        f.write("\n")
        for field in fields:
            f.write("echo \""+RUN_DIR+"/verif_"+model+"_"+field+".sh\" >> poescript\n")
        f.write("\n")
        f.write("\n")
        f.write("chmod 775 poescript\n")
        f.write("export MP_PGMMODEL=mpmd\n")
        f.write("export MP_CMDFILE=poescript\n")
        f.write("\n")
        f.write("echo beforelsf\n")

        if machine == 'WCOSS':
            f.write("mpirun.lsf poescript\n")
        elif machine == 'WCOSS_DELL_P3':
            pass
            f.write("mpirun -l cfp poescript\n")
        elif machine == 'WCOSS2':
            f.write("mpiexec -np "+str(ncpus)+" -ppn "+str(ncpus)+" --cpu-bind verbose,depth cfp poescript\n")

        f.write("echo afterlsf\n")
        f.write("\n")

        # Only run StatAnalysis once per day
        if (use_case == 'grid2grid_mrms' and valid_hour == 23) or \
           (use_case == 'grid2obs' and valid_hour == 21) or \
           (use_case == 'surrogate_severe'):

            f.write("\n")
            f.write("echo running StatAnalysis to combine data for valid date\n")
            f.write("export VDATE="+valid_time.strftime('%Y%m%d')+"\n")
            f.write("\n")

            f.write("run_metplus.py -c "+METPLUS_CONFIG_DIR+"/ldawson_"+system+".conf "+USE_CASE_DIR+"/"+stat_analysis_conf+" "+MODEL_CONF_DIR+"/"+model+".conf\n")
            f.write("\n")

            if 'gatherByDay' in stat_analysis_conf:
                STAT_ANALYSIS_FILE = model+'_'+valid_time.strftime('%Y%m%d')+'.stat'
            elif 'gatherByHour' in stat_analysis_conf:
                STAT_ANALYSIS_FILE = model+'_'+valid_time.strftime('%Y%m%d%H')+'.stat'

            f.write("\n")
            f.write("echo moving stat_analysis files to noscrub archive\n")
            f.write("mkdir -p "+STAT_ARCHIVE_DIR+"/\n")
            f.write("cp "+STAT_ANALYSIS_DIR+"/"+STAT_ANALYSIS_FILE+" "+STAT_ARCHIVE_DIR+"/\n")
            f.write("\n")
        
        f.write("exit\n")
        f.write("\n")

        f.close()





#########################################
#            BEGIN SCRIPT               #
#########################################


current_time = datetime.datetime.utcnow()

# Include option to define valid time on command line
# Used to backfill verification
try:
    vday = str(sys.argv[1])

    YYYY = int(vday[0:4])
    MM   = int(vday[4:6])
    DD   = int(vday[6:8])
    HH   = int(vday[8:19])

    valid_time = datetime.datetime(YYYY,MM,DD,HH,0,0)
except IndexError:
   vday = None


# Default to 24-hr verification lag if not defined on command line 
# Will adjust time for other use cases, if needed 
if vday is None:
    valid_time = current_time + datetime.timedelta(hours=-24)


# Get machine
#machine, hostname = dawsonpy.get_machine()
machine = 'WCOSS2'

# Set up working directory
if machine == 'WCOSS':
    VERIF_DIR = '/gpfs/'+hostname[0]+'d1/emc/meso/save/'+os.environ['USER']+'/CAM_verif'
elif machine == 'WCOSS_C':
    pass
elif machine == 'WCOSS2':
    system = 'cactus'
    SAVE_DIR = '/lfs/h2/emc/vpppg/save/'+os.environ['USER']+'/CAM_verif'
    NOSCRUB_DIR = '/lfs/h2/emc/vpppg/noscrub/'+os.environ['USER']+'/CAM_verif'
    PTMP_DIR = '/lfs/h2/emc/ptmp/'+os.environ['USER']+'/CAM_verif/METplus'
    FIX_DIR = '/lfs/h2/emc/vpppg/noscrub/emc.vpppg/verification/EVS_fix'
#   MASK_DIR = '/gpfs/dell2/emc/verification/noscrub/Julie.Prestopnik/met/9.0/share/met/poly/NCEP_masks'

# METplus version (needed for path to conf files)
METPLUS_VERSION = '4.1.4'

# Path to directory where system conf file lives
METPLUS_CONFIG_DIR = os.path.join(SAVE_DIR,'parm','metplus_config','METplus-'+METPLUS_VERSION)




#models = [str(sys.argv[1])]

HiResModels = ['CONUSARW','CONUSARW2','CONUSFV3','CONUSHREF_MEAN','CONUSHREFX_MEAN','CONUSHREF_PMMN','CONUSHREFX_PMMN','CONUSHREF_PROB','CONUSHREFX_PROB','CONUSNEST','CONUSNMMB','FV3LAM','FV3LAMDA','FV3LAMDAX','FV3LAMX','FV3SAR','FV3SARDA','FV3SARX','HRRR','HRRRX','RRFS_A','RRFS_A_CONUS','RRFS_A_NA']



# Define use case(s) to run based on valid time
valid_hour = int(valid_time.strftime('%H'))


'''
if valid_hour%3 == 0:
    use_cases = ['grid2grid_mrms','grid2obs']
    if valid_hour == 12:
        use_cases.extend(['surrogate_severe'])
else:
    use_cases = ['grid2grid_mrms']
'''
use_cases = ['grid2grid_mrms']


# Write scripts to run metplus and submit batch job

for use_case in use_cases:

    # Define models and verification grid for use case
    if use_case == 'grid2grid_mrms':
        vx_grid = 'G227'
        stat_analysis_conf = 'StatAnalysis_fcstCAM_obsMRMS_gatherByDay.conf'
        models = ['CONUSARW','CONUSARW2','CONUSFV3','CONUSHREF_PMMN','CONUSHREF_PROB','CONUSNEST','FV3LAMDAX','HRRR','RRFS_A_CONUS','RRFS_A_NA']
        models = ['CONUSARW','CONUSARW2','CONUSFV3','CONUSHREF_PMMN','CONUSNEST','FV3LAMDAX','HRRR','RRFS_A_CONUS','RRFS_A_NA']
    elif use_case == 'surrogate_severe':
        vx_grid = 'G211'
        stat_analysis_conf = 'StatAnalysis_fcstSSPF_obsPPF_gatherByDay.conf'
        models = ['CONUSARW','CONUSARW2','CONUSFV3','CONUSHREF_PROB','CONUSNEST','FV3LAMDA','FV3LAMDAX','HRRR','RRFS_A']
    elif use_case == 'grid2obs':
        vx_grid = 'G104'
        stat_analysis_conf = 'StatAnalysis_fcstCAM_obsNDAS_gatherByDay.conf'
        models = ['AKHREF_MEAN','AKHREFX_MEAN','CONUSHREF_MEAN','CONUSHREFX_MEAN','HIHREF_MEAN','HIHREFX_MEAN','PRHREF_MEAN','PRHREFX_MEAN']
        models = ['AKHREF_MEAN','CONUSHREF_MEAN']

    # Directory where use case conf files live
    USE_CASE_DIR = os.path.join(SAVE_DIR,'parm','use_cases','METplus-'+METPLUS_VERSION,use_case)


    # Path to directory where model conf files live
    if use_case == 'surrogate_severe':
        MODEL_CONF_DIR = os.path.join(SAVE_DIR,'parm','use_cases','METplus-'+METPLUS_VERSION,use_case,'model_configs')
        # Use 7-day lag to conduct verification if not defined on command line 
        if vday is None:
            valid_time = current_time + datetime.timedelta(hours=-168)

        valid_beg = valid_time + datetime.timedelta(hours=-24)
        valid_end = valid_time

    else:
        MODEL_CONF_DIR = os.path.join(SAVE_DIR,'parm','use_cases','METplus-'+METPLUS_VERSION,'model_configs')
        # Use 24-hr lag to conduct verification if not defined on command line 
        if vday is None:
            valid_time = current_time + datetime.timedelta(hours=-24)


    # Path to directory where mask files live
    MASK_DIR = os.path.join(PTMP_DIR,'metplus.out','masks',vx_grid)

    if not os.path.exists(MASK_DIR):
        os.makedirs(MASK_DIR)

    os.system('cp '+FIX_DIR+'/masks/Bukovsky_'+vx_grid+'*.nc '+MASK_DIR)


    # Define directory for StatAnalysis output
    STAT_ANALYSIS_DIR = os.path.join(PTMP_DIR,'metplus.out','stat_analysis',use_case,valid_time.strftime('%Y%m%d'))


    # Loop through models for each use case
    for model in models:

        # Set up run directories
        RUN_DIR = os.path.join(PTMP_DIR,'runscripts',use_case,model,valid_time.strftime('%Y%m%d%H'))
        if os.path.exists(RUN_DIR):
            shutil.rmtree(RUN_DIR)
        os.makedirs(RUN_DIR)
        os.chdir(RUN_DIR)

        # Define noscrub directory for StatAnalysis archive
      # STAT_ARCHIVE_DIR = os.path.join(NOSCRUB_DIR,'metplus_stat_archive',use_case,model,valid_time.strftime('%Y%m%d'))
        STAT_ARCHIVE_DIR = os.path.join(NOSCRUB_DIR,'metplus_stat_archive',use_case,model)

        # Define initial list of masking regions
        if str.upper(model[0:2]) == 'AK' or str.upper(model[-2:]) == 'AK':
            # List of Alaska masking files
            mask_str = MASK_DIR+'/NAK_'+vx_grid+'.nc\",\"'+MASK_DIR+'/SAK_'+vx_grid+'.nc' 

        elif str.upper(model[0:2]) == 'HI':
            continue
        elif str.upper(model[0:2]) == 'PR':
            continue

        else:
            # Initial list of CONUS masking files
            vx_masks = ['APL','GMC','GRB','LMV','MDW','NEC','NMT','NPL','NWC','SEC','SMT','SPL','SWC','SWD']
            vx_masks= ['CONUS_East','CONUS_West','CONUS_Central','CONUS_South']

            mask_str = MASK_DIR+'/Bukovsky_'+vx_grid+'_CONUS.nc'
            for vx_mask in vx_masks:
                mask_str = mask_str + '\",\"'+MASK_DIR+'/Bukovsky_'+vx_grid+'_'+vx_mask+'.nc' 


            # Define SPC outlook issuance time based on valid hour
            if valid_hour <= 12:
                day1_obj = valid_time + datetime.timedelta(hours=-24)
                day2_obj = valid_time + datetime.timedelta(hours=-48)
                day3_obj = valid_time + datetime.timedelta(hours=-72)
            elif valid_hour > 12:
                day1_obj = valid_time
                day2_obj = valid_time + datetime.timedelta(hours=-24)
                day3_obj = valid_time + datetime.timedelta(hours=-48)
    
            day1_issued = day1_obj.strftime('%Y%m%d')
            day2_issued = day2_obj.strftime('%Y%m%d')
            day3_issued = day3_obj.strftime('%Y%m%d')


            # Add SPC mask files to list if outlook(s) exists
            spc_outlooks = ['day1otlk_'+day1_issued+'_1200','day2otlk_'+day2_issued+'_1730','day3otlk_'+day3_issued]
            for otlk in spc_outlooks:
                search_path = MASK_DIR+'/SPC_outlooks/'+otlk+'*.nc'
                file_list = [f for f in glob.glob(search_path)]
                for mask in file_list:
                    otlk_ind = mask.find(otlk)
                    mask_str = mask_str + '\",\"'+MASK_DIR+'/SPC_outlooks/'+mask[otlk_ind:]

     #  print(mask_str)



        # Write scripts to call METplus for radar verification
        if use_case == 'grid2grid_mrms':

            if model in HiResModels:
                fields = ['refc','refd1','retop']
            else:
                fields = ['refc']

            wait_time = 0
            for field in fields:
                write_metplus_job()
                wait_time += 5
            fields_str = ', '.join(fields)
         #  print("Preparing to verify "+str.upper(model)+" "+fields_str+" valid at "+valid_time.strftime('%Y%m%d%H'))


        # Write scripts to call METplus for surrogate severe verification
        elif use_case == 'surrogate_severe':

            fields = ['SSPF']

            wait_time = 0
            for field in fields:
                write_metplus_job()
                wait_time += 5
            fields_str = 'SSPF'
            print("\n\nPreparing to verify "+str.upper(model)+" "+fields_str+" valid at "+valid_time.strftime('%Y%m%d%H')+"\n")


        # Write scripts to call METplus for grid2obs verification
        elif use_case == 'grid2obs':

            if str.upper(model[0:5]) == 'CONUS':
                pb2nc_grid = 'G212'
            elif str.upper(model[0:2]) == 'AK':
                pb2nc_grid = 'G236'

            fields = ['sfc_upper']

            wait_time = 0
            for field in fields:
                write_metplus_job()
                wait_time += 5
            fields_str = 'upper air and surface'
            print("\n\nPreparing to verify "+str.upper(model)+" "+fields_str+" valid at "+valid_time.strftime('%Y%m%d%H')+"\n")


        # Write and submit batch jobs
        print("\n\nPreparing to verify "+str.upper(model)+" "+fields_str+" valid at "+valid_time.strftime('%Y%m%d%H')+"\n")
        print(mask_str)
        write_batch_job(model, fields)
        job_script = RUN_DIR+'/verif_'+model+'.sh'
        dawsonpy.submit_job(job_script)



