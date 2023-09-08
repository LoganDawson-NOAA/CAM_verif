#!/bin/bash
# Author: L.C. Dawson
#
######################################################################
#            Cron script to download SPC storm reports               #
#           Submits job to calculate Practically Perfect             #
######################################################################


set -x

now=`date -u +%Y%m%d%H`

# Get the number of arguments.
NARGS=$#
ARGS=("$@")

# Read report date from command line, if provided (YYYYMMDD)
if [[ ${NARGS} -eq 1 ]]; then
   REPORT_DATE=$1
   REP_DATE=`echo ${REPORT_DATE} | cut -c 1-8`
   END_DATE=`date -d "${REP_DATE} + 1 day" '+%Y%m%d'`
   REP_MONTH=`echo ${REPORT_DATE} | cut -c 1-6`

   # Define environment variables for METplus job
   export SPC_DATE=`echo ${REPORT_DATE} | cut -c 3-8`
   export ACCUM_BEG=`echo ${REP_DATE}`12
   export ACCUM_END=`echo ${END_DATE}`12

# Else, use 8-day lag
else
   REPORT_DATE=`$NDATE -192 $now | cut -c 1-8`
   END_DATE=`$NDATE -168 $now | cut -c 1-8`
   REP_MONTH=`echo ${REPORT_DATE} | cut -c 1-6`

   # Define environment variables for METplus job
   export SPC_DATE=${REPORT_DATE:2-8}
   export ACCUM_BEG=${REPORT_DATE:0-8}12
   export ACCUM_END=${END_DATE:0-8}12
fi


# Define directory where to download/write CSV files
REPORT_DIR=/lfs/h2/emc/ptmp/${USER}/CAM_verif/METplus/metplus.out/surrogate_severe/spc_reports
mkdir -p ${REPORT_DIR}
cd $REPORT_DIR

REP_FILE=${SPC_DATE}_rpts_filtered.csv
if [ -f "$REP_FILE" ]; then
   rm $REP_FILE
fi

echo "Downloading file listing all reports"
wget https://www.spc.noaa.gov/climo/reports/${REP_FILE}

HAZARDS="torn hail wind"
for HAZARD in $HAZARDS; do
   echo "Downloading file listing $HAZARD reports"

   REP_FILE=${SPC_DATE}_rpts_filtered_${HAZARD}.csv
   if [ -f "$REP_FILE" ]; then
      rm $REP_FILE
   fi

   wget https://www.spc.noaa.gov/climo/reports/${REP_FILE}
done

#
# Prepare to process LSRs and generate PPF

# Set METplus version to use
METPLUS_VERSION=4.1.1

# Set some necessary directory paths
SAVE_DIR=/lfs/h2/emc/vpppg/save/${USER}/CAM_verif
NOSCRUB_DIR=/lfs/h2/emc/vpppg/noscrub/${USER}/CAM_verif/surrogate_severe/point2grid/${REP_MONTH}
POINT2GRID_DIR=/lfs/h2/emc/ptmp/${USER}/CAM_verif/METplus/metplus.out/surrogate_severe/point2grid

# Set and change to directory where script will run
RUN_DIR=/lfs/h2/emc/ptmp/${USER}/CAM_verif/METplus/runscripts/surrogate_severe/ppf/${REPORT_DATE}
mkdir -p ${RUN_DIR}
cd ${RUN_DIR}

# Set script name
jobname=gen_ppf
#PBS -R "affinity[core]"
#PBS -R "rusage[mem=1500]"
#PBS -n 16
#PBS -R span[ptile=16]

cat > $RUN_DIR/${jobname}.sh <<EOF
#!/bin/ksh
#
#PBS -N ${jobname}
#PBS -o ${RUN_DIR}/ppf.out
#PBS -e ${RUN_DIR}/ppf.err
#PBS -l walltime=00:45:00
#PBS -l select=1:ncpus=1:mem=1500MB
#PBS -A VERF-DEV
#PBS -q dev 
#
set +x

. ~/dots/dot.for.metplus-${METPLUS_VERSION}

set -x

export SPC_DATE=$SPC_DATE
export ACCUM_BEG=$ACCUM_BEG
export ACCUM_END=$ACCUM_END

# Generate Practically Perfect Forecast
master_metplus.py -c ${SAVE_DIR}/parm/metplus_config/METplus-${METPLUS_VERSION}/ldawson_cactus.conf ${SAVE_DIR}/parm/use_cases/METplus-${METPLUS_VERSION}/surrogate_severe/Point2Grid_obsLSR_PracticallyPerfect.conf


# Copy gridded data to noscrub 
mkdir -p ${NOSCRUB_DIR}
cp ${POINT2GRID_DIR}/*${ACCUM_END}_G211.nc ${NOSCRUB_DIR} 


# Plot output
${SAVE_DIR}/plotting/plot_ppf.sh $REPORT_DATE


exit

EOF


qsub ${RUN_DIR}/${jobname}.sh


exit

