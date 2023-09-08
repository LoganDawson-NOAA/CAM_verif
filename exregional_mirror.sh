#!/bin/sh
#############################################################################
# Script name:          exfv3cam_cleanup.sh
# Script description:   Scrub old files and directories
# Script history log:
#   1) 2018-04-09       Ben Blake
#                       new script
#############################################################################
set -x

MODEL=$1
USE_CASE=$2


hostname > hname
hl=`cut -c 1-1 hname`

if [ $hl = v ] ; then
  opshost=mars
fi
if [ $hl = m ] ; then
  opshost=venus
fi

STAT_ARCH=/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/metplus_stat_archive




ssh -l ${USER} ${opshost}.ncep.noaa.gov "mkdir -p ${STAT_ARCH}/${USE_CASE}/${MODEL}"
cd ${STAT_ARCH}/${USE_CASE}/${MODEL}

scp ${MODEL}_20211019.stat $USER@${opshost}.ncep.noaa.gov:${STAT_ARCH}/${USE_CASE}/${MODEL}/.


exit
