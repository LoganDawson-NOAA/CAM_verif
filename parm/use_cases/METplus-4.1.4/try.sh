
set +x
. ~/dots/dot.for.metplus-3.1

set -x

echo running StatAnalysis to combine data for valid hour
export VDATE=20210430

master_metplus.py -c /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/metplus_config/METplus-3.1/ldawson_dell.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.1/grid2obs/StatAnalysis_fcstCAM_obsNDAS_gatherByDay.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.1/model_configs/CONUSHREF_MEAN.conf

