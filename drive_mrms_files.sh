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

mrms_job=$1

cd /lfs/h2/emc/vpppg/save/${USER}/CAM_verif/

python mrms_${mrms_job}.py 

exit
