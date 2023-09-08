
set +x
. ~/dots/dot.for.metplus-3.1

set -x

#export SPC_DATE=200412
export ACCUM_BEG=2021020712
export ACCUM_END=2021020712
export HWT_THRESH=25

#cd /gpfs/dell2/ptmp/Logan.Dawson/CAM_verif/METplus/metplus.out/surrogate_severe/spc_reports/

master_metplus.py -c /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/metplus_config/METplus-3.1/ldawson_dell.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.1/surrogate_severe/EnsembleStat_fcstCAM_SurrogateSevere.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.1/model_configs/CONUSNMMB.conf

#master_metplus.py -c /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/metplus_config/METplus-3.1/ldawson_dell.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.1/surrogate_severe/EnsembleStat_fcstHREF_FcstOnly_NetCDF.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.1/model_configs/CONUSHREF.conf


#master_metplus.py -c /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/metplus_config/METplus-3.1/ldawson_dell.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.1/surrogate_severe/EnsembleStat_fcstHREF_FcstOnly_NetCDF.conf /gpfs/dell2/emc/verification/save/Logan.Dawson/CAM_verif/parm/use_cases/METplus-3.1/model_configs/CONUSHREFX.conf
