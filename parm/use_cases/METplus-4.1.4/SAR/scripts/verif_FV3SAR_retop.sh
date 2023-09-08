#!/bin/bash
#
sleep 10
. ~/dots/dot.for.metplus-3.0

cd /gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/runscripts/FV3SAR/2020030200

export VDATE=2020030200
export MASKS="/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/CONUS_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/APL_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/GMC_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/GRB_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/LMV_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/MDW_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/NEC_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/NMT_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/NPL_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/NWC_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/SEC_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/SMT_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/SPL_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/SWC_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/SWD_G227.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/SPC_outlooks/day1otlk_20200301_1200_cat_Rec0_TSTM_mask.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/SPC_outlooks/day2otlk_20200229_1730_cat_Rec0_TSTM_mask.nc","/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/masks/SPC_outlooks/day3otlk_20200228_0830_cat_Rec0_TSTM_mask.nc"

/gpfs/dell2/emc/verification/save/Logan.Dawson/METplus-3.0-beta2/ush/master_metplus.py -c /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/metplus_config/METplus-3.0/ldawson_dell.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.0/grid2grid_mrms/GridStat_fcstCAM_obsMRMS_RETOP.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.0/grid2grid_mrms/FV3SAR.conf

exit

