#!/usr/bin/env python
import netCDF4
from scipy import ndimage, signal
import numpy as np
import os, datetime
import dawsonpy

# Get necessary information from environment
valid = os.environ['DATE']
grid = os.environ['TOGRID']
#valid = '2020030615'
#grid = 'G227'

YYYY = int(valid[0:4])
MM = int(valid[4:6])
DD = int(valid[6:8])
HH = int(valid[8:10])


# Get machine
machine, hostname = dawsonpy.get_machine()

# Set up working directory
if machine == 'WCOSS':
    pass
elif machine == 'WCOSS_C':
    pass
elif machine == 'WCOSS_DELL_P3':
    VERIF_DIR = '/gpfs/dell2/emc/verification/save/'+os.environ['USER']+'/CAM_verif'
    DATA_HEAD = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/com/MRMS'
    REGRID_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/CAM_verif/METplus/metplus.out/regrid/'+str.upper(grid)+'/MRMS/'+valid[0:8]



#################################### Set Constant Attributes:  #####################################################

file_origins = 'NA'
met_version = 'V9.0'
met_tool = 'regrid_data_plane'

if str.upper(grid) == 'G227':
    projection = 'Lambert Conformal'
    hemisphere= 'N'
    scale_lat_1 = '25.00000'
    scale_lat_2 = '25.00000'
    lat_pin = '12.190000'
    lon_pin = '-133.459000'
    x_pin = '0.000000'
    y_pin = '0.000000'
    lon_orient = '-95.000000'
    d_km = '5.079000'
    r_km = '6371.200000'
    nx = '1473'
    ny = '1025 grid_points'

lat_long_name = 'latitude'
lat_units = 'degrees_north'
lat_standard_name = 'latitude'

lon_long_name = 'longitude'
lon_units = 'degrees_east'
lon_standard_name = 'longitude'



#################################### Read Data  #####################################################

obs_names = ['MergedReflectivityQCComposite','SeamlessHSR','EchoTop18']
obs_long_names = ['Composite Reflectivity Mosaic (optimal method)','Seamless Hybrid Scan Reflectivity with VPR correction','Echo Top - 18 dBZ']


for obs_name in obs_names:

    i = obs_names.index(obs_name)

    # Level for SeamlessHSR differs
    if obs_name == 'SeamlessHSR':
        obs_level = 'L0'
        level = '00.00'
    else:
        obs_level = 'Z500'
        level = '00.50'

    # Units for EchoTop18 differs
    if obs_name == 'EchoTop18':
        fname = 'EchoTop18'
        obs_units = 'km MSL'
        thresholds = [20,30,40]
    else:
        fname = obs_name
        obs_units = 'dBZ'
        thresholds = [20,30,40,50]

    try:
        fil = netCDF4.Dataset(REGRID_DIR+'/'+fname+'_'+level+'_'+valid[0:8]+'-'+valid[8:10]+'0000_'+str.lower(grid)+'.nc', 'r')
    except IOError:
        print("No "+valid[8:10]+"Z "+valid[0:8]+" "+obs_name+" file on G227. Moving on to next product.")
        continue

    xlat = fil.variables['lat'][:]
    xlon = fil.variables['lon'][:]

    if obs_name == 'EchoTop18':
        obs = fil.variables[obs_name][:]*3280.84 * 0.001   # convert from km to kft
    else:
        obs = fil.variables[obs_name][:]


  # Read init and valid time attributes from input file
  # nc_variable = fil.variables[obs_name]
  # init_time = netCDF4.Dataset.getncattr(nc_variable,'init_time')
  # init_time_ut = fil.getncattr(obs_name,'init_time_ut')
  # valid_time = fil.getncattr(obs_name,'valid_time')
  # valid_time_ut = fil.getncattr(obs_name,'valid_time_ut')

    fil.close()

    # Directly definte init and valid time attributes
    epoch = (datetime.datetime(YYYY,MM,DD,HH,00,00) - datetime.datetime(1970,1,1)).total_seconds()
    init_time = valid[0:8]+'_'+valid[8:10]+'0000'
    init_time_ut = str(epoch)
    valid_time = init_time
    valid_time_ut = init_time_ut

#################################### Calculate NBMAX ObProb Field  #####################################################

    # Calculate neighborhood max
    nbmax = ndimage.maximum_filter(obs, size=17, mode='nearest')

    # Define kernel for convolution
    y,x = np.ogrid[-5:5+1, -5:5+1]
    kernel = x**2 + y**2
    # Define binary field based on threshold exceedances in max field
    # Calculate observed probability
    bin_obs = []
    obprobs = []
    for threshold in thresholds:
        nbmax_thresh = np.where(nbmax>threshold,1,0)
        bin_obs.append(nbmax_thresh)
        obprob = ndimage.gaussian_filter(signal.fftconvolve(nbmax_thresh,kernel,mode='same'),sigma=5,mode='nearest')/kernel.sum()
        obprobs.append(obprob)
        print(np.min(obprob),np.max(obprob))

### op40 = ndimage.gaussian_filter(nbmax40, sigma=5, mode='nearest')
### op40 = ndimage.gaussian_filter(signal.fftconvolve(nbmax40,kernel,mode='same'),sigma=5,mode='nearest')
### op40 = signal.fftconvolve(ndimage.gaussian_filter(nbmax40,sigma=5,mode='nearest'),kernel,mode='same')
  # op40 = ndimage.gaussian_filter(signal.fftconvolve(nbmax40,kernel/float(kernel.sum()),mode='same'),sigma=5,mode='nearest')
  # op40 = ndimage.gaussian_filter(signal.fftconvolve(nbmax20,kernel,mode='same'),sigma=5,mode='nearest')/kernel.sum()


#################################### Write Data  #####################################################


    outfile = REGRID_DIR+'/'+obs_name+'_NBMAX_'+valid[0:8]+'-'+valid[8:10]+'0000_'+str.lower(grid)+'.nc'

    try:
        fout = netCDF4.Dataset(outfile, "w")
    except:
        print("Could not create %s!\n" % outfile)

    fout.createDimension('lat',xlat.shape[0])
    fout.createDimension('lon',xlat.shape[1])

    setattr(fout,'FileOrigins',file_origins)
    setattr(fout,'MET_version',met_version)
    setattr(fout,'MET_tool',met_tool)
    setattr(fout,'Projection',projection)
    setattr(fout,'scale_lat_1',scale_lat_1)
    setattr(fout,'scale_lat_2',scale_lat_2)
    setattr(fout,'lat_pin',lat_pin)
    setattr(fout,'lon_pin',lon_pin)
    setattr(fout,'x_pin',x_pin)
    setattr(fout,'y_pin',y_pin)
    setattr(fout,'lon_orient',lon_orient)
    setattr(fout,'d_km',d_km)
    setattr(fout,'r_km',r_km)
    setattr(fout,'nx',nx)
    setattr(fout,'ny',ny)

    lat_out = fout.createVariable('lat', 'f4', ('lat','lon',))
    lon_out = fout.createVariable('lon', 'f4', ('lat','lon',))
    obs_out = fout.createVariable(obs_name, 'f4', ('lat','lon',), fill_value = -9999.)
    obs_out = fout.createVariable(obs_name+'_MaxFilter', 'f4', ('lat','lon',), fill_value = -9999.)

    fout.variables['lat'][:] = xlat
    fout.variables['lon'][:] = xlon
    fout.variables[obs_name][:] = obs
    fout.variables[obs_name+'_MaxFilter'][:] = nbmax

    lat_out.long_name = lat_long_name
    lat_out.units = lat_units
    lat_out.standard_name = lat_standard_name

    lon_out.long_name = lon_long_name
    lon_out.units = lon_units
    lon_out.standard_name = lon_standard_name

    obs_out.setncattr('name', obs_name) #need to use setncattr for special case of 'name'
    obs_out.long_name = obs_long_names[i]
    obs_out.level = obs_level
    obs_out.units = obs_units

    obs_out.setncattr('name', obs_name+'_MaxFilter') #need to use setncattr for special case of 'name'
    obs_out.long_name = obs_long_names[i]
    obs_out.level = obs_level
    obs_out.units = obs_units
    obs_out.init_time = init_time
    obs_out.init_time_ut = init_time_ut
    obs_out.valid_time = valid_time
    obs_out.valid_time_ut = valid_time_ut

    for j in range(len(obprobs)):

        bin_out = fout.createVariable(obs_names[i]+'_Bin'+str(thresholds[j]), 'f4', ('lat','lon',), fill_value = -9999.)
        fout.variables[obs_names[i]+'_Bin'+str(thresholds[j])][:] = bin_obs[j]
        bin_out.setncattr('name',obs_names[i]+'_Bin'+str(thresholds[j])) #need to use setncattr for special case of 'name'
        bin_out.long_name = obs_long_names[i]+' Binary > '+str(thresholds[j])
        bin_out.level = obs_level
        bin_out.units = obs_units
        bin_out.init_time = init_time
        bin_out.init_time_ut = init_time_ut
        bin_out.valid_time = valid_time
        bin_out.valid_time_ut = valid_time_ut

        obprob_out = fout.createVariable(obs_names[i]+'_Prob'+str(thresholds[j]), 'f4', ('lat','lon',), fill_value = -9999.)
        fout.variables[obs_names[i]+'_Prob'+str(thresholds[j])][:] = obprobs[j]
        obprob_out.setncattr('name',obs_names[i]+'_Prob'+str(thresholds[j])) #need to use setncattr for special case of 'name'
        obprob_out.long_name = obs_long_names[i]+' Probability > '+str(thresholds[j])
        obprob_out.level = obs_level
        obprob_out.units = obs_units
        obprob_out.init_time = init_time
        obprob_out.init_time_ut = init_time_ut
        obprob_out.valid_time = valid_time
        obprob_out.valid_time_ut = valid_time_ut


    fout.close()

