#!/bin/bash
#PBS -N xfer
#PBS -j oe
#PBS -A VERF-DEV
#PBS -l select=1:ncpus=1:mem=50GB
#PBS -q dev_transfer
#PBS -l walltime=00:45:00

cd $PBS_O_WORKDIR


scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/save/logan.dawson/CAM_verif/plotting/*.sh /lfs/h2/emc/vpppg/save/logan.dawson/MEG/CAM_verif_plotting/

scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/save/logan.dawson/CAM_verif/plotting/*.py /lfs/h2/emc/vpppg/save/logan.dawson/MEG/CAM_verif_plotting/

scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/save/logan.dawson/MEG/* /lfs/h2/emc/vpppg/save/logan.dawson/MEG


#scp ldawson@emcrzdm:/home/people/emc/www/htdocs/users/verification/regional/cam/cam_ops.surr_svr.webpage.tar.gz /lfs/h2/emc/vpppg/noscrub/logan.dawson 


#scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/prep/*.gz /lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/prep

#scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/stats/*.gz /lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/stats

exit

#scp /lfs/h2/emc/vpppg/noscrub/logan.dawson/CAM_verif/masks/Bukovsky_CONUS/EVS_fix/Alaska_G221.nc logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/noscrub/logan.dawson/CAM_verif/masks/Bukovsky_CONUS/EVS_fix/Alaska_G221.nc

#scp /lfs/h2/emc/vpppg/noscrub/logan.dawson/CAM_verif/masks/Bukovsky_CONUS/EVS_fix/*G221*.nc Logan.Dawson@dtn-hera.fairmont.rdhpcs.noaa.gov:/scratch2/NCEPDEV/ovp/Logan.Dawson


#scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/u/logan.dawson/*.py /u/logan.dawson



#scp Logan.Dawson@dtn-jet.boulder.rdhpcs.noaa.gov:/mnt/lfs4/HFIP/hwrfv3/Logan.Dawson/parse_adeck.py /lfs/h2/emc/stmp/logan.dawson




#scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/prep/cam/atmos/prep.tar.gz /lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/prep/cam/atmos

#scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/save/logan.dawson/test_EVS/*.sh /lfs/h2/emc/vpppg/save/logan.dawson/test_EVS




#/lfs/h2/emc/vpppg/noscrub/logan.dawson/CAM_verif/mask.tar /lfs/h2/emc/vpppg/noscrub/logan.dawson/CAM_verif/mask.tar

#scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/u/logan.dawson/cam_verif.tar /u/logan.dawson/cam_verif.tar

#mkdir -p /lfs/h2/emc/vpppg/save/logan.dawson/python/
#scp logan.dawson@cdxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/save/logan.dawson/python/dawsonpy.py /lfs/h2/emc/vpppg/save/logan.dawson/python/dawsonpy.py



