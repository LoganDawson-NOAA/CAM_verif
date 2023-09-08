#!/bin/ksh --login
#
#BSUB -J verif_fv3sar
#BSUB -o /gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/runscripts/FV3SAR/2020030200/fv3sar.out
#BSUB -e /gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/runscripts/FV3SAR/2020030200/fv3sar.err
#BSUB -W 00:30
#BSUB -n 64
#BSUB -R span[ptile=16]
#BSUB -P HRW-T2O
#BSUB -q "dev_shared" 
#BSUB -R "affinity[core]"
#BSUB -R "rusage[mem=1500]"
#
set -x
. ~/dots/dot.for.metplus-3.0

module load lsf/10.1
module load impi/18.0.1
module load CFP/2.0.1

echo "/gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/runscripts/FV3SAR/2020030200/verif_FV3SAR_refc.sh" >> poescript
echo "/gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/runscripts/FV3SAR/2020030200/verif_FV3SAR_refd1.sh" >> poescript
echo "/gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/runscripts/FV3SAR/2020030200/verif_FV3SAR_retop.sh" >> poescript


chmod 775 poescript
export MP_PGMMODEL=mpmd
export MP_CMDFILE=poescript

echo beforelsf
mpirun -l cfp poescript
echo afterlsf


echo running StatAnalysis to combine REFC, REFD1, and RETOP data
export VDATE=20200302
export VHOUR=00

/gpfs/dell2/emc/verification/save/Logan.Dawson/METplus-3.0-beta2/ush/master_metplus.py -c /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/metplus_config/METplus-3.0/ldawson_dell.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.0/grid2grid_mrms/StatAnalysis_fcstCAM_obsMRMS_gatherByHour.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.0/grid2grid_mrms/FV3SAR.conf


echo moving stat_analysis files to noscrub archive
cp /gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/metplus.out/stat_analysis/grid2grid_mrms/20200302/FV3SAR_2020030200.stat /gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/metplus_stat_archive/grid2grid_mrms/FV3SAR/20200302/

exit

