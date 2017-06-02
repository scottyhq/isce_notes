#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create processing directories for all consecutive pairs given a directory of S1 zip files
ISCE VERSION: 201704

Usage: prep_sequential_processing.py datadir/

@author: scott
"""
import argparse
import glob
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

import prep_topsApp


def cmdLineParse():
    '''
    Command line parser.
    '''

    parser = argparse.ArgumentParser( description='prep_sequential_processing.py')
    parser.add_argument('-p', type=str, dest='path', required=True,
            help='Path to S1 data (zip files)')
    parser.add_argument('-s', type=int, dest='separation', #required=True,
            default=1,
            help='s=1 for sequential pairs (e.g. 12 day), s=2 skip 1 date (e.g. 24 day)')
    parser.add_argument('-n', type=int, nargs='+', dest='swaths', #required=True,
            default=[1,2,3], #NOTE passed as variable number of ints: -n 1 2
            help='Subswath number to process')
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


def create_dataframe(inps):
    '''
    Gather S1 zip files into pandas data frame 
    '''
    datadir = inps.path
    paths = glob.glob(os.path.join(datadir,'S1*zip'))
    zips = [os.path.basename(x) for x in paths]
    zips.sort() #chronological order
    timestamps = [x.split('_')[5] for x in zips]
    dates = [x.split('T')[0] for x in timestamps]
    df = pd.DataFrame(dict(file=zips))
    df['date'] = pd.to_datetime(dates)
    #df['gmt'] = #get time if desired
    df['satellite'] = df.file.str[:3]
    df['ones'] = 1    
    
    DF  = df.ix[:,['date','satellite']].drop_duplicates('date').reset_index(drop=True)
    DF.sort_values(by='date', inplace=True)
    DF['dt'] = DF.date.diff()
    n = len(DF)
    print('Total acquisitions: ', n)
    print(DF)
    DF.to_csv('acquisitions.csv')
    
    return df, DF


def create_processing_directories(df,DF,inps):
    '''
    Create a bunch of directories for topsApp.py
    '''
    
    for i in range(len(DF)-inps.separation):
        inps.slave = DF.date.iloc[i].strftime('%Y%m%d')
        inps.master = DF.date.iloc[i+inps.separation].strftime('%Y%m%d')
        intdir = 'int_{0}_{1}'.format(inps.master, inps.slave)
        os.mkdir(intdir)
        os.chdir(intdir)
        #df.query('date == @master')['file'].tolist()
        inps.master_scenes = prep_topsApp.find_scenes(inps.path, inps.master)
        inps.slave_scenes = prep_topsApp.find_scenes(inps.path, inps.slave)
        prep_topsApp.write_topsApp_xml(inps)
        os.chdir('../')


def create_figure(df,DF,inps):
    '''
    Graphical representation of pairs to make
    '''
    #Neater
    dfA  = df.query('satellite == "S1A"').drop_duplicates('date').reset_index(drop=True)
    dfB  = df.query('satellite == "S1B"').drop_duplicates('date').reset_index(drop=True)
    print('S1A acquisitions: ', len(dfA))
    print('S1B acquisitions: ', len(dfB))

    fig,ax = plt.subplots(figsize=(12,4))
    plt.plot(dfA.date, dfA.ones, 'mo', label='S1A')
    plt.plot(dfB.date, dfB.ones, 'co', label='S1B')
    plt.legend()
    plt.yticks([1,],[''])
    plt.ylim(0,2)
    
    #NOTE: could annotate full dates with vertical text
    '''
    for i,row in DF.iterrows():
        #print(row.date, row.date.strftime('%Y-%m-%d'))
        plt.text(row.date, 0.9, row.date.strftime('%m-%d'), 
                 ha='center',
                 rotation=90)
    '''
        
    #show connections
    n = len(DF)
    for i in range(n-inps.separation):
        # Sequential (e.g. 12 day)
        ann = ax.annotate('', xy=(DF.date.iloc[i], 1.), xycoords='data',
                      xytext=(DF.date.iloc[i+inps.separation], 1), textcoords='data',
                      arrowprops=dict(arrowstyle="-",connectionstyle="arc3,rad=0.8"),
                      )
        
    ax = plt.gca()
    ax.xaxis.set_minor_locator(MonthLocator())
    ax.xaxis.set_major_locator(YearLocator())
    ax.fmt_xdata = DateFormatter('%Y-%m-%d')
    fig.autofmt_xdate()
    plt.title('Acquisitions={}, Pairs={}'.format(n, n-inps.separation))
    plt.savefig('acquisition_timeline.pdf', bbox_inches='tight')





if __name__ == '__main__':
    inps = cmdLineParse()
    #ensure absolute paths
    inps.path = os.path.abspath(inps.path)
    inps.dem = os.path.abspath(inps.dem)
    inps.auxdir = os.path.abspath(inps.auxdir)
    inps.orbitdir = os.path.abspath(inps.orbitdir)

    df,DF = create_dataframe(inps)
    create_processing_directories(df,DF,inps)
    create_figure(df,DF,inps)
    

