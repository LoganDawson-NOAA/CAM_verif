#!/usr/bin/env python
import numpy as np
import sys, os, datetime
import shutil
import netCDF4
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpl_toolkits
mpl_toolkits.__path__.append('/gpfs/dell3/ptmp/py/lib/python/basemap-1.2.1-py3.6-linux-x86_64.egg/mpl_toolkits/')
from mpl_toolkits.basemap import Basemap, cm
import dawsonpy


# Get necessary information from environment
try:
    valid = str(sys.argv[1])
except IndexError:
    valid = None

if valid is None:
    valid = os.environ['DATE']


YYYY = int(valid[0:4])
MM = int(valid[4:6])
DD = int(valid[6:8])
HH = int(valid[8:10])

valid_end = datetime.datetime(YYYY,MM,DD,HH,00,00)


# Get machine
machine, hostname = dawsonpy.get_machine()

# Set up working directory
if machine == 'WCOSS':
    pass
elif machine == 'WCOSS_C':
    pass
elif machine == 'WCOSS_DELL_P3':
    system = 'dell'
    SAVE_DIR = '/gpfs/dell2/emc/verification/save/'+os.environ['USER']+'/CAM_verif'
    NOSCRUB_DIR = '/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif'
    OUT_DIR = NOSCRUB_DIR+'/surrogate_severe/'+valid_end.strftime('%Y%m%d%H')
    SCRIPT_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/CAM_verif/METplus'
    PTMP_DIR = '/gpfs/dell2/ptmp/'+os.environ['USER']+'/UH_accums/'+valid_end.strftime('%Y%m%d%H')+'/surrogates'

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

if not os.path.exists(PTMP_DIR):
    os.makedirs(PTMP_DIR)


# METplus version (needed for path to conf files)
METPLUS_VERSION = '3.0'

# Path to directory where system conf file lives
METPLUS_CONFIG_DIR = os.path.join(SAVE_DIR,'parm','metplus_config','METplus-'+METPLUS_VERSION)

# Path to directory where use case files live
use_case = 'surrogate_severe'
USE_CASE_DIR = os.path.join(SAVE_DIR,'parm','use_cases','METplus-'+METPLUS_VERSION,use_case)

# Path to directory where model conf files live
MODEL_CONF_DIR = os.path.join(SAVE_DIR,'parm','use_cases','METplus-'+METPLUS_VERSION,use_case,'model_configs')

# Path to directory to G211 data lives
#REGRID_DIR = os.path.join(SCRIPT_DIR,'metplus.out','regrid','G211')

# Path to directory to write job scripts
RUN_DIR = os.path.join(SCRIPT_DIR,'runscripts',use_case,valid_end.strftime('%Y%m%d%H'))

# Set up run directory
if not os.path.exists(RUN_DIR):
    os.makedirs(RUN_DIR)
os.chdir(RUN_DIR)





href_mems  = ['HiResWARW_lag','HiResWARW2_lag','HiResWNMMB_lag','NAM3_lag','HiResWARW','HiResWARW2','HiResWNMMB','NAM3']
hrefx_mems = ['HiResWARW_lag','HiResWARW2_lag','HiResWFV3_lag','HRRR_lag','NAM3_lag','HiResWARW','HiResWARW2','HiResWFV3','HRRR','NAM3']


#################################### Set Constant Attributes:  #####################################################

file_origins = 'NA'
met_version = 'V9.0'
met_tool = 'regrid_data_plane'

projection = 'Lambert Conformal'
hemisphere= 'N'
scale_lat_1 = '25.00000'
scale_lat_2 = '25.00000'
lat_pin = '12.190000'
lon_pin = '-133.459000'
x_pin = '0.000000'
y_pin = '0.000000'
lon_orient = '-95.000000'
d_km = '81.271000'
r_km = '6371.200000'
nx = '93'
ny = '65 grid_points'

lat_long_name = 'latitude'
lat_units = 'degrees_north'
lat_standard_name = 'latitude'

lon_long_name = 'longitude'
lon_units = 'degrees_east'
lon_standard_name = 'longitude'


valid_beg = valid_end + datetime.timedelta(hours=-24)

# Suffix for files with G211 surrogate
file_suffix = '.UHmax-24h.'+valid_beg.strftime('%Y%m%d%H')+'-'+valid_end.strftime('%Y%m%d%H')+'_SSPF.nc'



############################## Calculate 24-h UH max for HREF members  ############################################
###################################### Write to netCDF files  #####################################################

ensembles = ['HREF_00Z','HREFX_00Z','HREF_12Z','HREFX_12Z']
members = [href_mems, hrefx_mems]


for ensemble in ensembles:

    i = ensembles.index(ensemble)%2
    ens_list = []
    filelist = []

    print(ensemble[-3:]+' '+ensemble[:-4])

    # Define initialization time for HREF run
    if ensemble[-3:] == '00Z':
        href_init_time = valid_end + datetime.timedelta(hours=-36)
    elif ensemble[-3:] == '12Z':
        href_init_time = valid_end + datetime.timedelta(hours=-24)
    

    for member in members[i]:

        # Define init times and forecast hours for 00Z and 12Z HREF "on-time"  members
        if str.upper(ensemble[-3:]) == '00Z' and str.lower(member[-3:]) != 'lag':
            fhr = 36
        elif str.upper(ensemble[-3:]) == '12Z' and str.lower(member[-3:]) != 'lag':
            fhr = 24

        # Define init times and forecast hours for 00Z HREF lagged members
        elif str.upper(ensemble[-3:]) == '00Z' and str.lower(member[-3:]) == 'lag':
            if str.upper(member[0:6]) == 'HIRESW':
                fhr = 48
            elif str.upper(member[:-4]) == 'NAM3' or str.upper(member[:-4]) == 'HRRR':
                fhr = 42

        # Define init times and forecast hours for 12Z HREF lagged members
        elif str.upper(ensemble[-3:]) == '12Z' and str.lower(member[-3:]) == 'lag':
            if str.upper(member[0:6]) == 'HIRESW':
                fhr = 36
            elif str.upper(member[:-4]) == 'NAM3' or str.upper(member[:-4]) == 'HRRR':
                fhr = 30


        init_time = valid_end + datetime.timedelta(hours=-fhr)
        if str.lower(member[-3:]) == 'lag':
            print(init_time.strftime('%HZ %m/%d')+' '+member[:-4])
        else:
            print(init_time.strftime('%HZ %m/%d')+' '+member)
        


        if str.upper(member[0:10]) == 'HIRESWARW2':
            mem_prefix = 'hiresw.t'
            mem_prefix2 = 'hiresw.'
            mem_suffix = 'z.arw_5km.f'+str(fhr).zfill(2)+'.conusmem2'
            MET_MODEL_NAME = 'CONUSARW2'

        elif str.upper(member[0:9]) == 'HIRESWARW':
            mem_prefix = 'hiresw.t'
            mem_prefix2 = 'hiresw.'
            mem_suffix = 'z.arw_5km.f'+str(fhr).zfill(2)+'.conus'
            MET_MODEL_NAME = 'CONUSARW'

        elif str.upper(member[0:9]) == 'HIRESWFV3':
            mem_prefix = 'hiresw.t'
            mem_prefix2 = 'hiresw.'
            mem_suffix = 'z.fv3_5km.f'+str(fhr).zfill(2)+'.conus'
            MET_MODEL_NAME = 'CONUSFV3'

        elif str.upper(member[0:10]) == 'HIRESWNMMB':
            mem_prefix = 'hiresw.t'
            mem_prefix2 = 'hiresw.'
            mem_suffix = 'z.nmmb_5km.f'+str(fhr).zfill(2)+'.conus'
            MET_MODEL_NAME = 'CONUSNMMB'

        elif str.upper(member[0:4]) == 'HRRR':
            mem_prefix = 'hrrr.t'
            mem_prefix2 = 'hrrr.'
            mem_suffix = 'z.wrfprsf'+str(fhr).zfill(2)
            MET_MODEL_NAME = 'HRRR'

        elif str.upper(member[0:4]) == 'NAM3':
            mem_prefix = 'nam.t'
            mem_prefix2 = 'nam.'
            mem_suffix = 'z.conusnest.hiresf'+str(fhr).zfill(2)+'.tm00'
            MET_MODEL_NAME = 'CONUSNEST'


        fil = OUT_DIR+'/'+mem_prefix2+init_time.strftime('%Y%m%d')+'.t'+init_time.strftime('%H')+mem_suffix+file_suffix
        print(fil)

        filelist.append(fil)

    # Check to see if all necessary forecast hour files exist
    file_size = 50000 
    files_exist = [True if os.path.exists(fil) and os.stat(fil).st_size > file_size else False for fil in sorted(filelist)]


    # Loop through to read data and plot member SSPF
    for fil in sorted(filelist):

        # Skip plotting if the expected file doesn't exist
        if files_exist[filelist.index(fil)] == False:
            continue

        # Open netcdf file and read UH variable
     #  fil = OUT_DIR+'/'+mem_prefix2+init_time.strftime('%Y%m%d')+'.t'+init_time.strftime('%H')+mem_suffix+file_suffix
        print(fil)
        nc = netCDF4.Dataset(fil,'r')
        data = nc.variables['UH_SSPF'][:]

        lats = nc.variables['lat'][:]
        lons = nc.variables['lon'][:]

        # Build list of 24-h UH accumulations for each member
        ens_list.append(data)


        fig = plt.figure(figsize=(10.9,8.9))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])

        m = Basemap(llcrnrlon=-121.5,llcrnrlat=22.,urcrnrlon=-64.5,urcrnrlat=48.,\
                    resolution='i',projection='lcc',\
                    lat_1=32.,lat_2=46.,lon_0=-101.,area_thresh=1000.,ax=ax)

        m.drawcoastlines()
        m.drawstates(linewidth=0.75)
        m.drawcountries()
        latlongrid = 10.
        parallels = np.arange(-90.,91.,latlongrid)
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
        meridians = np.arange(0.,360.,latlongrid)
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)


        clevs = [2,5,10,15,30,45,60,70,80,90,95]
        colorlist = ['blue','dodgerblue','cyan','limegreen','chartreuse','yellow', \
                     'orange','red','darkred','purple','orchid']

        fill_var = data*100.
        fill = m.contourf(lons,lats,fill_var,clevs,latlon=True,colors=colorlist,extend='max')
        cbar = plt.colorbar(fill,ax=ax,ticks=clevs,orientation='horizontal',pad=0.04,shrink=0.75,aspect=20)
        cbar.set_label('%')

        filename = fil[88:-3]

        if str.lower(filename[0:6]) == 'hiresw':
            if 'arw' in str.lower(filename) and 'mem2' in str.lower(filename):
                plot_name = 'HiResW ARW2'
            elif 'arw' in str.lower(filename):
                plot_name = 'HiResW ARW'
            elif 'fv3' in str.lower(filename):
                plot_name = 'HiResW FV3'
            elif 'nmmb' in str.lower(filename):
                plot_name = 'HiResW NMMB'
        elif str.lower(filename[0:4]) == 'hrrr':
            plot_name = 'HRRR'
        elif str.lower(filename[0:3]) == 'nam':
            plot_name = 'NAM Nest'
        



        init_str = href_init_time.strftime('Init: %HZ %d %b %Y') 
        valid_str  = valid_beg.strftime('Valid: %HZ %m/%d/%y')+valid_end.strftime(' to %HZ %m/%d/%y (F'+str(fhr).zfill(2)+')')
        plt.text(0, 1.06, plot_name+' Surrogate Severe Forecast', fontweight='bold', horizontalalignment='left', transform=ax.transAxes)
        plt.text(0, 1.01, '(based on 24-h max 2-5 km UH)', fontweight='bold', horizontalalignment='left', transform=ax.transAxes)
        plt.text(1, 1.06, init_str, fontweight='bold', horizontalalignment='right', transform=ax.transAxes)
        plt.text(1, 1.01, valid_str, fontweight='bold', horizontalalignment='right', transform=ax.transAxes)

      # filename = mem_prefix2+init_time.strftime('%Y%m%d')+'.t'+init_time.strftime('%H')+mem_suffix+'.UHmax-24h.'+valid_beg.strftime('%Y%m%d%H')+'-'+valid_end.strftime('%Y%m%d%H')+'_SSPF' 
        plt.savefig(PTMP_DIR+'/'+filename+'.png',bbox_inches='tight')
        plt.close()



    # If any files are missing, skip to next HREF init without working
    if any(files_exist) is False:
        print('At least one file is missing. Can\'t create SSPF for '+ensemble[-3:]+' '+ensemble[:-4]+'.')
        continue

    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]

    # Calculate neighborhood max ensemble probability at each gridpoint
    nmep = np.mean(np.array(ens_list),axis=0)
    nmep[nmep < 0.] = 0.

    print(np.amin(nmep),np.amax(nmep))



    # Write data to a netcdf file
    # Define output file name
    outfile = OUT_DIR+'/'+str.lower(ensemble[:-4])+'.'+href_init_time.strftime('%Y%m%d')+'.t'+href_init_time.strftime('%H')+'z.conus.nmep.f'+str(fhr).zfill(2)+'.'+valid_beg.strftime('%Y%m%d%H')+'-'+valid_end.strftime('%Y%m%d%H')+'_SSPF.nc' 

    try:
        fout = netCDF4.Dataset(outfile, "w")
    except:
        print("Could not create %s!\n" % outfile)


    fout.createDimension('lat',lats.shape[0])
    fout.createDimension('lon',lats.shape[1])

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
    var_out = fout.createVariable('UH_SSPF', 'f4', ('lat','lon',), fill_value = -9999.)

    fout.variables['lat'][:] = lats
    fout.variables['lon'][:] = lons
    fout.variables['UH_SSPF'][:] = nmep

    lat_out.long_name = lat_long_name
    lat_out.units = lat_units
    lat_out.standard_name = lat_standard_name

    lon_out.long_name = lon_long_name
    lon_out.units = lon_units
    lon_out.standard_name = lon_standard_name

    var_out.setncattr('name', 'UH_SSPF') #need to use setncattr for special case of 'name'
    var_out.long_name = 'Surrogate severe probability forecast (NMEP of 24-h max 2-5 km UH)'
    var_out.level = 'Z2000-5000'
    var_out.units = '%'

    init_time_ut  = (href_init_time - datetime.datetime(1970,1,1)).total_seconds()
    valid_time_ut = (valid_end - datetime.datetime(1970,1,1)).total_seconds()
    var_out.init_time = href_init_time.strftime('%Y%m%d_%H%M%S')
    var_out.init_time_ut = str(init_time_ut)
    var_out.valid_time = valid_end.strftime('%Y%m%d_%H%M%S')
    var_out.valid_time_ut = str(valid_time_ut)

    fout.close()


    fig = plt.figure(figsize=(10.9,8.9))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])

    m = Basemap(llcrnrlon=-121.5,llcrnrlat=22.,urcrnrlon=-64.5,urcrnrlat=48.,\
                resolution='i',projection='lcc',\
                lat_1=32.,lat_2=46.,lon_0=-101.,area_thresh=1000.,ax=ax)

    m.drawcoastlines()
    m.drawstates(linewidth=0.75)
    m.drawcountries()
    latlongrid = 10.
    parallels = np.arange(-90.,91.,latlongrid)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    meridians = np.arange(0.,360.,latlongrid)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

    fill_var = nmep*100.

    clevs = [2,5,10,15,30,45,60,70,80,90,95]
    colorlist = ['blue','dodgerblue','cyan','limegreen','chartreuse','yellow', \
                 'orange','red','darkred','purple','orchid']

    fill = m.contourf(lons,lats,fill_var,clevs,latlon=True,colors=colorlist,extend='max')
    cbar = plt.colorbar(fill,ax=ax,ticks=clevs,orientation='horizontal',pad=0.04,shrink=0.75,aspect=20)
    cbar.set_label('%')

    init_str = href_init_time.strftime('Init: %HZ %d %b %Y') 
    valid_str  = valid_beg.strftime('Valid: %HZ %m/%d/%y')+valid_end.strftime(' to %HZ %m/%d/%y (F'+str(fhr).zfill(2)+')')
    plt.text(0, 1.06, ensemble[:-4]+' Surrogate Severe Forecast', fontweight='bold', horizontalalignment='left', transform=ax.transAxes)
    plt.text(0, 1.01, '(based on 24-h max 2-5 km UH)', fontweight='bold', horizontalalignment='left', transform=ax.transAxes)
    plt.text(1, 1.06, init_str, fontweight='bold', horizontalalignment='right', transform=ax.transAxes)
    plt.text(1, 1.01, valid_str, fontweight='bold', horizontalalignment='right', transform=ax.transAxes)

    filename = str.lower(ensemble[:-4])+'.'+href_init_time.strftime('%Y%m%d')+'.t'+href_init_time.strftime('%H')+'z.conus.'+valid_beg.strftime('%Y%m%d%H')+'-'+valid_end.strftime('%Y%m%d%H')+'_SSPF' 
    plt.savefig(PTMP_DIR+'/'+filename+'.png',bbox_inches='tight')
    plt.close()







