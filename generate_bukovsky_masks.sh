#
###################################################
# Generate CONUS-only Bukovsky vx masking regions #
###################################################

set -x

MET_DIR=/gpfs/dell2/emc/verification/noscrub/emc.metplus/met/10.0.0
MASK_DIR=/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks


# Create CONUS mask on Bukovsky grid 
${MET_DIR}/exec/gen_vx_mask -type poly ${MASK_DIR}/bukovsky/CPlains.nc ${MET_DIR}/share/met/poly/CONUS.poly ${MASK_DIR}/bukovsky/updated_regions/CONUS.nc



# Create CONUS subregion masks

POLYS=(PacificNW PacificSW Southwest Mezquital NRockies SRockies GreatBasin NPlains CPlains SPlains Prairie GreatLakes Appalachia DeepSouth Southeast MidAtlantic NorthAtlantic)

for (( i=0; i<=${#POLYS[*]}-1; i ++ )); do
   ${MET_DIR}/exec/gen_vx_mask -type data -intersection ${MASK_DIR}/bukovsky/${POLYS[$i]}.nc ${MASK_DIR}/bukovsky/updated_regions/CONUS.nc ${MASK_DIR}/bukovsky/updated_regions/${POLYS[$i]}.nc -mask_field 'name="CONUS";' -thresh 'eq1' -name ${POLYS[$i]} -v 5

done


exit
