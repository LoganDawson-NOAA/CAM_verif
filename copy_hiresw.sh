#!/bin/bash
# Author: L.C. Dawson
#
#######################################################################
# Cron script to handle MRMS files for verification and HPSS          #
# Takes one argument to define which python script to run:            #
#    'copy' - copies MRMS files from dcom and unzip for verification  #
#    'archive' - zips and archives MRMS files to HPSS                 #
#######################################################################

set +x

source ~/.bashrc

set -x

now=`date -u +%Y%m%d%H`
HiResWs="HiResWARW HiResWARW2 HiResWFV3"

cd /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/

# Get 00Z runs on 6-day lag
CYCLE=`$NDATE -144 $now | cut -c 1-10`
for HIRESW in $HiResWs; do
    python copy_hiresw.py $CYCLE $HIRESW
done

# Get 12Z runs on 6-day lag
CYCLE=`$NDATE -132 $now | cut -c 1-10`
for HIRESW in $HiResWs; do
    python copy_hiresw.py $CYCLE $HIRESW
done


exit
