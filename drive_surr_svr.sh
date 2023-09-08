#!/bin/bash
# Author: L.C. Dawson
#
#######################################################################
# Cron script to handle MRMS files for verification and HPSS          #
# Takes one argument to define which python script to run:            #
#    'copy' - copies MRMS files from dcom and unzip for verification  #
#    'archive' - zips and archives MRMS files to HPSS                 #
#######################################################################


#METPLUS_VERSION='3.1'

set +x
. ~/.bashrc
set -x


# Get the number of arguments.
NARGS=$#
ARGS=("$@")

# Use valid date passed in on command line
if [[ ${NARGS} -eq 1 ]]; then
   VALID_END=$1
else
   # If no command line argument passed in,
   # Set valid end time to 12Z on current day
   # Cron job starts at 0100 UTC
   now=`date -u +%Y%m%d%H`
   VALID_END=`$NDATE 11 $now | cut -c 1-10`
fi

cd /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/


# Writes scripts to generate 24-h SSPFs for all models 
# 1. Run PcpCombine DERIVE MAX to generate 24-h UH swaths on native grids 
# 2. Run EnsembleStat to generate surrogates on 81-km grid 
# 3. Run RegridDataPlane to generate deterministic SSPFs
# 4. Run EnsembleState and RegridDataPlane to generate HREF SSPFs
# 5. Plot all output
python drive_surr_svr.py ${VALID_END}


# Calculate UH threshold values for 24-h UH accumulations 
# Write to annual CSV files
#python calc_uh_percentiles.py ${VALID_END}




exit

