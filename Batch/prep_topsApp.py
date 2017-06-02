#!/usr/bin/env python
'''
Make symbolic links and topsApp.xml in order to create an interferogram
with topsApp.py (ISCE 2.0.0_201704

Examples:
# process just subswaths 1 and 2
prep_topsApp.py -m 20160910 -s 20160724 -p /media/hdd2/data/insar/sentinel/colombia_north/A150 -n 1 2

prep_topsApp.py -m 20160910 -s 20160724 -p ../data/A150 -n 1 -r 4.3 5.3 -75.6 -74.6 -d /home/data/dems/srtmGL1/colombia/demLat_S04_N12_Lon_W081_W070.dem.wgs84

Author Scott Henderson
'''
import argparse
import os
import glob
#import pprint

import isce
from isceobj.XmlUtil import FastXML as xml


def cmdLineParse():
    '''
    Command line parser.
    '''

    parser = argparse.ArgumentParser( description='prep topsApp.py')
    parser.add_argument('-m', type=str, dest='master', required=True,
            help='Master date')
    parser.add_argument('-s', type=str, dest='slave', required=True,
            help='Slave date')
    parser.add_argument('-p', type=str, dest='path', required=True,
            help='Path to S1 data (zip files)')
    parser.add_argument('-n', type=int, nargs='+', dest='swaths', required=True,
            help='Subswath numbers to process')
    parser.add_argument('-d', type=str, dest='dem', required=False,
            help='Path to DEM file')
    parser.add_argument('-o', type=str, dest='orbitdir', required=False,
            default='/22t1/common_data/s1_poeorb',
            help='Orbit directory')
    parser.add_argument('-a', type=str, dest='auxdir', required=False,
            default='/22t1/common_data/s1_auxcal',
            help='Auxilary file directory')
    parser.add_argument('-r', type=float, nargs=4, dest='roi', required=False,
            help='Region of interest bbox [S,N,W,E]')
    parser.add_argument('-g', type=float, nargs=4, dest='gbox', required=False,
            help='Geocode bbox [S,N,W,E]')

    return parser.parse_args()
    

def find_scenes(datadir, date):
    files = glob.glob(os.path.join(datadir,'S1*_{}*zip'.format(date)))
    files.sort()
    filenames = [os.path.basename(f) for f in files]
    
    # create symlinks
    for f in files:
        os.symlink(f, os.path.basename(f))
    
    return filenames

def write_topsApp_xml(inps):
    ''' use built in isce utility to write XML programatically (based on unoffical isce guide Sep2014'''
    insar = xml.Component('topsinsar')
    common = {}
    common['orbit directory'] = inps.orbitdir
    common['auxiliary data directory'] = inps.auxdir
    #common['swath number'] = inps.subswath
    if inps.roi:
        common['region of interest'] = inps.roi
    master = {}
    master['safe'] = inps.master_scenes 
    master['output directory'] = 'masterdir'
    master.update(common)
    slave = {}
    slave['safe'] = inps.slave_scenes
    slave['output directory'] = 'slavedir'
    slave.update(common)
    #####Set sub-component
    insar['master'] = master
    insar['slave'] = slave
    ####Set properties
    #insar['doppler method'] = 'useDEFAULT' only insarApp
    insar['sensor name'] = 'SENTINEL1'
    insar['do unwrap'] = True
    insar['unwrapper name'] = 'snaphu_mcf'
    insar['swaths'] = inps.swaths
    if inps.gbox:
        insar['geocode bounding box'] = inps.gbox
        # Just essentials for batch processing
        insar['geocode list'] = ['merged/filt_topophase.unw.conncomp','merged/filt_topophase.unw','merged/phsig.cor']
    if inps.dem:
        insar['demfilename'] = inps.dem
    #####Catalog example
    #insar['dem'] = xml.Catalog('dem.xml') #Components include a writeXML method
    insar.writeXML('topsApp.xml', root='topsApp')
    

    
if __name__ == '__main__':
    inps = cmdLineParse()
    #print(inps)
    intdir = 'int_{0}_{1}'.format(inps.master, inps.slave)
    os.mkdir(intdir)
    os.chdir(intdir)
    inps.master_scenes = find_scenes(inps.path, inps.master)
    inps.slave_scenes = find_scenes(inps.path, inps.slave)
    write_topsApp_xml(inps)
    print('Ready to run topsApp.py in {}'.format(intdir))
