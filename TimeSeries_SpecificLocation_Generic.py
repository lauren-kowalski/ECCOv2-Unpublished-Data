#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 10:39:48 2023

@author: laurenkowalski

Algorithm to download data from ECCO drive and plot:

This code is to create a time series from ECCO drive data at a specific
location of your choosing.

This can be edited to develop a time series at the surface or at depth.

***You must have .data & .meta datafiles and geographic files (XC/XG/YC/YG/ZC/ZG) saved in your 
directory.***

Review ZG.data for depth steps to determine which depth you want to analyze.

"""
#import applicable modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from MITgcmutils import rdmds
import os
import glob

#=============================================================================
# Generating List of Files Downloaded to Create Relevant DataFrames 
#=============================================================================
#change directory
os.chdir('your working directory')

#creating MMMYY/TimeStepInterval dataframe #NEED TO CREATE WAY TO DO THIS WITH CODE!
df = pd.read_excel('MMMYY_TimeStepInt.xlsx')

#create searchable file list with values from Time Step Interval
a = glob.glob("your working directory/<name of files you want to list>")
b = []
for i in a:
    b.append(os.path.basename(i))
b.sort()
#print(b)  #uncomment as a check

#isolating the timestep interval from the file name
r = [f[17:24] for f in b]  #fill in with your date element range for your files
timeint = []
for i in r:
    s = int(float(i))
    timeint.append(s)
#print(timeint)  #uncomment as a check

#identify MMMYY from filename generate list using the .xlsx # NEED TO DO THIS WITH NEW DATAFRAME
MMMYY = []
for x in timeint:
    l = (df.loc[df.TimeStepInterval == x, 'MMMYY'].values[0])
    MMMYY.append(l)
#print(MMMYY)  #uncomment as a check
    
location = 'if desired - location name of region'

#Geographic Boundaries - NW Siple Island
MinLat = (<your minlat>); MaxLat = (<your maxlat>)
MinLon = (<your minlon>); MaxLon = (<your maxlon>)

#=============================================================================
# Tracer Concentration Time Series 
#=============================================================================
#change directory
os.chdir('your working directory')
    
#generate wvel for each file name
Zconc = []
for z in timeint:
    #reading in relevant datafile and isolating applicable tracer at a 
    #specified depth
    tr123 = rdmds('state_3d_set3',z);
    tr1 = tr123[0,:,:,:] #surface signature
    #tr2 = tr123[1,:,:,:] #cdw signature - uncomment and edit zcon to reflect tr2
    #tr3 = tr123[2,:,:,:] #meltwater signature - uncomment and edit zcon to reflect tr3
    zcon = tr1[19,:,:].copy() #z=19 correlates to 248m depth
    #creating geographic bounds
    XC=rdmds('XC');YC=rdmds('YC');
    AmundsenSeaLat = (MinLat < YC) & (YC < MaxLat)
    AmundsenSeaLon = (MinLon < XC) & (XC < MaxLon)
    AmundsenSea = AmundsenSeaLat & AmundsenSeaLon
    #naning out all FALSE
    zcon[~(AmundsenSea)]=np.nan
    zcon = np.nanmean(zcon) #calc mean of Zcon in area
    Zconc.append(zcon)
#print(wvelocity) #uncomment as a check

#read in zconc dataframe
zdf = pd.DataFrame({'MMMYY':MMMYY, 'Zconc':Zconc})
zdf.info()

#=============================================================================
# Vertical Velocity Time Series 
#=============================================================================
#change directory
os.chdir('your working directory')
   
#generate wvel for each file name
wvelocity = []
for y in timeint:
    #reading in relevant datafile and isolating applicable vertical velocity at a specified depth
    TSUVW = rdmds('state_3d_set2',y); #reading in file
    U = TSUVW[2,:,:,:] #E-W velocities - uncomment and edit vel to reflect U
    V = TSUVW[3,:,:,:] #N-S velocities - uncomment and edit vel to reflect V
    W = TSUVW[4,:,:,:] #vertical velocities
    vel = W[19,:,:].copy() #z=19 correlates to 248m depth
    #creating geographic bounds
    XC=rdmds('XC');YC=rdmds('YC');
    AmundsenSeaLat = (MinLat < YC) & (YC < MaxLat)
    AmundsenSeaLon = (MinLon < XC) & (XC < MaxLon)
    AmundsenSea = AmundsenSeaLat & AmundsenSeaLon
    #naning out all FALSE
    vel[~(AmundsenSea)]=np.nan
    vel = np.nanmean(vel) #calc mean of Zcon in area
    wvelocity.append(vel)
#print(wvelocity) #uncomment as a check

os.chdir('your working directory')

#create wdf = wvel dataframe
wdf = pd.DataFrame({'MMMYY':MMMYY, 'w':wvelocity})
wdf.info()

#=============================================================================
# Plotting Time Series Against Each Other
#=============================================================================

fig, ax1 = plt.subplots(figsize=(15,7))

#Tracer Concentration Plot
color = 'tab:green'
ax1.set_xlabel('Time')
ax1.set_ylabel('Tracer X Concentration') #update for which tracer you are plotting
ax1.plot(zdf['MMMYY'],zdf['Zconc'], marker='*', color=color, linewidth=0.5)
ax1.tick_params(axis='y')
for label in ax1.get_xticklabels():
    label.set_rotation(315)
    label.set_ha('left')
ax1.legend(['Tracer 1 Concentration'])
ax1.set_title('<Date Range> Tracer X Time Series - '+location+' Subset') #update 
#for which date range you are plotting and for which tracer you are plotting
ax1.grid()
#Vertical Velocities Plot
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
##ax2.yaxis.set_major_locator(LinearLocator(N))
color = 'tab:red'
ax2.tick_params(axis='y')
ax2.set_ylabel('<Direction> Velocities (m/s)', rotation=270)  # we already 
#handled the x-label with ax1,update with direction of velocities
ax2.plot(zdf['MMMYY'],wdf['w'], marker='h', color=color, linewidth=0.5) #xaxis must remain the same
ax2.legend(['Vertical Velocities'])
fig.align_ylabels()
plt.tight_layout()
plt.savefig('your working directory/<filename>.png') #update file name accordingly
plt.show()


