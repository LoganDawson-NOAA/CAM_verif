#!/bin/bash
# Author: L.C. Dawson
#
#####################################
# Generate CONUS vx masking regions #
#####################################

set -x

MET_DIR=/gpfs/dell2/emc/verification/noscrub/emc.metplus/met/10.0.0
MASK_DIR=/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks
TOGRID=$1

mkdir -p ${MASK_DIR}/${TOGRID}

#POLYS=(NEC SEC APL GMC MDW LMV NPL SPL NMT SMT SWD GRB NWC SWC CONUS EAST WEST NAK SAK)
POLYS=(NEC SEC APL GMC MDW LMV NPL SPL NMT SMT SWD GRB NWC SWC CONUS EAST WEST)

# Create CONUS subregion masks
for (( i=0; i<=${#POLYS[*]}-1; i ++ )); do
   ${MET_DIR}/exec/gen_vx_mask -type poly ${MASK_DIR}/grid_files/${TOGRID}.nc ${MET_DIR}/share/met/poly/${POLYS[$i]}.poly ${MASK_DIR}/${TOGRID}/${POLYS[$i]}_${TOGRID}.nc
#  ${MET_DIR}/bin/gen_vx_mask -type grid ${MASK_DIR}/grid_files/${TOGRID}.nc ${MET_DIR}/share/met/poly/NCEP_masks/${POLYS[$i]}_mask.nc ${MASK_DIR}/${TOGRID}/${POLYS[$i]}_${TOGRID}.nc

done


# Create CONUS mask by iteratively taking union of all subregions 
#infile=${MASK_DIR}/${TOGRID}/NEC_${TOGRID}.nc
#for (( i=1; i<=${#POLYS[*]}-1; i ++ )); do
#   ${MET_DIR}/bin/gen_vx_mask $infile ${MET_DIR}/share/met/poly/${POLYS[$i]}.poly ${MASK_DIR}/${TOGRID}/temp.nc
#   infile=${MASK_DIR}/${TOGRID}/temp.nc
#done

#mv ${MASK_DIR}/${TOGRID}/temp.nc ${MASK_DIR}/${TOGRID}/CONUS_${TOGRID}.nc

exit
