#!/bin/bash
# Author: L.C. Dawson
#
###########################################################
# Called on a cron to run METplus verification every hour #
###########################################################

set +x

source ~/.bashrc

set -x

VDATE=$1

cd /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/

VHOURS="00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23"

for VHOUR in $VHOURS; do

   valid_date=${VDATE}${VHOUR}

   echo "Submitting veriification jobs for ${valid_date}"
   python href_rerun.py ${valid_date} 

done

exit
