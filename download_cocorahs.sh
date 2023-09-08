#!/bin/bash
# Author: L.C. Dawson

set +x

source ~/.bashrc

set -x

now=`date -u +%Y%m%d%H`

# Get the number of arguments.
NARGS=$#
ARGS=("$@")

# Check for at least 3 arguments
if [[ ${NARGS} -eq 1 ]]; then
   report_date=$1
else
   report_date=`$NDATE -48 $now | cut -c 1-8`
fi

YYYY=`echo $report_date | cut -c 1-4`
MM=`echo $report_date | cut -c 5-6`
DD=`echo $report_date | cut -c 7-8`


mkdir -p /lfs/h2/emc/ptmp/${USER}/com/cocorahs

cd /lfs/h2/emc/ptmp/${USER}/com/cocorahs


wget -O cocorahs.${YYYY}${MM}${DD}.dailyprecip.csv "http://data.cocorahs.org/export/exportreports.aspx?ReportType=Daily&dtf=2&Date=${MM}/${DD}/${YYYY}&TimesInGMT=True"

exit

