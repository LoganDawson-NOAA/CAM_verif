#!/bin/bash
#PBS -N xfer
#PBS -j oe
#PBS -A VERF-DEV
#PBS -l select=1:ncpus=1:mem=10GB
#PBS -q dev_transfer
#PBS -l walltime=00:45:00


cd $PBS_O_WORKDIR

#scp logan.dawson@ddxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/stats/*.gz /lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/stats/

scp logan.dawson@ddxfer.wcoss2.ncep.noaa.gov:/lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/prep/*.gz /lfs/h2/emc/vpppg/noscrub/logan.dawson/evs/v1.0/prep/

exit

#scp ${jet}:/mnt/lfs4/HFIP/hwrfv3/Logan.Dawson/olivia_plots.tar.gz /lfs/h2/emc/vpppg/noscrub/logan.dawson/olivia_plots.tar.gz
#scp ${hera}:/scratch2/NCEPDEV/ovp/Logan.Dawson/olivia_plots.tar.gz /lfs/h2/emc/vpppg/noscrub/logan.dawson/olivia_plots.tar.gz

