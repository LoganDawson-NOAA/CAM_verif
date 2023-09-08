#!/bin/bash
# Author: L.C. Dawson
#
###########################################################
# Called on a cron to run METplus verification every hour #
###########################################################

set +x

source ~/.bashrc

set -x

now=`date -u +%Y%m%d%H`
valid_date=`$NDATE -24 $now | cut -c 1-8`

cd /lfs/h2/emc/vpppg/save/logan.dawson/CAM_verif/

echo "Submitting veriification jobs for ${valid_date}"

python drive_metplus.py 

exit
