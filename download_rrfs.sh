#!/bin/sh -l
# Authors: L. Dawson

set -x

# Get the number of arguments.
NARGS=$#
ARGS=("$@")

# Get DATE from command line if argument exists 
if [[ ${NARGS} -ge 1 ]]; then
   DATE=$1
else
   # Use current date if no command line argument
   DATE=`date -u +%Y%m%d%H`
fi

YYYY=${DATE:0:4}
PDY=${DATE:0:8}
CYC="00"

COMROOT=/gpfs/dell2/ptmp/Logan.Dawson/com
mkdir -p ${COMROOT}

DATA_DIR=${COMROOT}/rrfs.${PDY}
mkdir -p ${DATA_DIR}

cd ${DATA_DIR}

AWS_HEAD="https://noaa-rrfs-pds.s3.amazonaws.com/rrfs.${PDY}/${CYC}"

if [[ ${NARGS} -eq 2 ]]; then
   mems="$2"
else
   # Use current date if no command line argument
   mems="01 02 03 04 05 06 07 08 09"
fi

for mem_num in $mems; do
   MEM_DIR=mem${mem_num}

   fhr=0
   while [ $fhr -le 60 ]; do

      FFF=$(printf "%03d" ${fhr})
      filename="rrfs.t${CYC}z.mem${mem_num}.naf${FFF}.grib2"
      fhr=$(($fhr+1))

   done

done

full=${AWS_HEAD}/${MEM_DIR}/${filename}
echo ${full}

wget ${full}
