#!/bin/sh -l
# Authors: J.H. Gotway and L. Dawson

set +x
. ~/dots/dot.for.metplus-4.0.0

set -x

# Get the number of arguments.
NARGS=$#
ARGS=("$@")

# Get SWODY from command line if argument exists 
if [[ ${NARGS} -eq 1 ]]; then
   SWODY=$1
else
   # Use current date if no command line argument
   SWODY=`date -u +%Y%m%d%H`
fi

YYYY=${SWODY:0:4}
PDY=${SWODY:0:8}


# Set up directory to save daily mask files
GRID_DIR="/gpfs/dell2/emc/verification/noscrub/${USER}/CAM_verif/masks"
MASK_DIR="/gpfs/dell2/ptmp/${USER}/CAM_verif/METplus/metplus.out/masks"
mkdir -p ${MASK_DIR}

# List of grids to create masks
GRIDS="G227 G211 G104"

# List of categories
CATS="TSTM MRGL SLGT ENH MOD HIGH"

# Grab Day 1 outlook at 08 UTC
#if [[ ${SWODY:8:2} == "08" ]]; then
#   day_start=1
#   day_end=1
# Grab Day 2 and Day 3 outlooks at 18 UTC
#elif [[ ${SWODY:8:2} == "18" ]]; then
#   day_start=2
#   day_end=3
#fi

# Loop over outlooks for days 1, 2, 3
#for ((DAY=$day_start;DAY<=$day_end;DAY++)); do
for DAY in {1..3}; do

  # Pull outlooks for the current day 
  #   https://www.spc.noaa.gov/products/outlook/day1otlk-shp.zip
  TEMP_DIR="/gpfs/dell2/ptmp/Logan.Dawson/day${DAY}otlk"
  rm -rf ${TEMP_DIR}
  mkdir -p ${TEMP_DIR}
  cd ${TEMP_DIR}

  if [[ ${DAY} == 1 ]]; then
      OTLK='1200'
  elif [[ ${DAY} == 2 ]]; then
      OTLK='1730'
  elif [[ ${DAY} == 3 ]]; then
      OTLK='0830'
   #  OTLK='0730'
  fi

  wget https://www.spc.noaa.gov/products/outlook/archive/${YYYY}/day${DAY}otlk_${PDY}_${OTLK}-shp.zip
  unzip day${DAY}otlk_${PDY}_${OTLK}-shp.zip
  SHP_FILE=day${DAY}otlk_${PDY}_${OTLK}_cat

  N_REC=`gis_dump_dbf ${SHP_FILE}.dbf | grep n_records | cut -d'=' -f2 | tr -d ' '`
  echo "Processing $N_REC records."

  # This doesn't currently do anything really... the next loop is simply skipped if no general thunder area is defined.
  if [[ $N_REC == 0 ]]; then
    echo "No Day ${DAY} Outlook areas issued on ${PDY}"
  fi

  # Loop over records and create a new mask for each
  N_REC_MINUS_1=$(($N_REC - 1))
  for REC in $(seq 0 $N_REC_MINUS_1); do
  for TOGRID in $GRIDS; do

    NAME=`gis_dump_dbf ${SHP_FILE}.dbf | egrep -A 5 "^Record ${REC}" | tail -1 | cut -d'"' -f2`
    echo "Processing Record Number $REC: $NAME"

    # Make sure output directory exists
    mkdir -p ${MASK_DIR}/${TOGRID}/SPC_outlooks

    GRID_NAME=${GRID_DIR}/grid_files/${TOGRID}.nc
    MASK_NAME=${SHP_FILE}_Rec${REC}_${NAME}_mask

    if [[ ${DAY} == 3 ]]; then
       gen_vx_mask ${GRID_NAME} ${SHP_FILE}.shp ${MASK_NAME}.nc -type shape -shapeno ${REC} -name DAY${DAY}_${NAME} -v 3 
    else
       gen_vx_mask ${GRID_NAME} ${SHP_FILE}.shp ${MASK_NAME}.nc -type shape -shapeno ${REC} -name DAY${DAY}_${OTLK}_${NAME} -v 3 
    fi

    cp ${MASK_NAME}.nc ${MASK_DIR}/${TOGRID}/SPC_outlooks/${MASK_NAME}.nc

  done
  done

done 


# Copy CONUS vx masks to ptmp directory
# Allows METplus to search for mask files in ptmp
# Rather than creating large archive of SPC masks in noscrub
for TOGRID in $GRIDS; do

   cp ${GRID_DIR}/${TOGRID}/*.nc ${MASK_DIR}/${TOGRID}

done 

exit
