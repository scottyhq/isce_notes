#!/usr/bin/env python3
import os
import glob

def run_topsApp_sequential():
    '''
    for now, simple external system call, run one at a time
    '''
    intDirs = glob.glob('int*')
    intDirs.sort() #chronological order
    print(len(intDirs), 'interferograms to be made...')
    
    for i,intdir in enumerate(intDirs):
        print('\n--------\n',i,intdir,'\n--------\n')
        os.chdir(intdir)
        if not os.path.exists('./merged'):
            os.system('topsApp.py --steps 2>&1 | tee topsApp.log')
            
            #Keep only merged/ directory to save space, keep xml files
            os.system('rm -r coarse_coreg coarse_interferogram coarse_offsets ESD fine_coreg fine_interferogram fine_offsets geom_master slavedir masterdir')  
            if i > 1: #keep geometry files onlt for first date to save space
                cmd = 'rm {0}/dem.crop* {0}/lat.rdr* {0}/lon.rdr* {0}/los.rdr {0}/los.rdr.full* {0}/z.rdr*'.format('merged')
                os.system(cmd)
        else:
            print(intdir, '"merged" folder already exists... skipping')
        os.chdir('../')

if __name__ == '__main__':
    run_topsApp_sequential()
