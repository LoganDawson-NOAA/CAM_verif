
import re, csv, glob


DATA_DIR = '/gpfs/dell2/emc/verification/noscrub/Logan.Dawson/CAM_verif/metplus_stat_archive/grid2grid_mrms'
days = ['20200222','20200223']
models = [ "CONUSARW", "CONUSARW2", "CONUSFV3", "CONUS_HREFPMMN", "CONUS_HREFPMMNX", "CONUSNEST", "CONUSNMMB", "FV3SAR", "FV3SARX", "HRRR" ]


for day in days:
    for model in models:

        filelist = [f for f in glob.glob(DATA_DIR+'/'+day+'/'+str.upper(model)+'_'+day+'*.stat')]
        datelist = [filelist[x][-15:-5] for x in range(len(filelist))]

        for date in datelist:

            print(date)

            writefile = open(DATA_DIR+'/testing/'+str.upper(model)+'_'+date+'.stat','wt')


            with open(DATA_DIR+'/'+day+'/'+str.upper(model)+'_'+date+'.stat','r') as f:
                for line in f:
                    if re.search('DAY2_TSTM',line):
                        pass
                    else:
                        writefile.writelines(line)
            
            
            writefile.close()
            print('Done filtering '+date+' '+model+' file')

