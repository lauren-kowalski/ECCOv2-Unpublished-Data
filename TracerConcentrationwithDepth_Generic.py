#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:29:40 2023

@author: laurenkowalski

For 1 year, observe seasonality of tracer concentrations and vertical velocity
at depth (between 250-500m)

"""

#import xarray as xr #used to read and plot the downloaded NetCDF files
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from MITgcmutils import rdmds
import os
import calendar

#=============================================================================
# Creating TimeStep Module
#=============================================================================
#verify directory
os.chdir('your working directory')

#define start year of data
year = <start year of data>

#create empty lists for appending...
days = [] #for number of days in a month (to include leap years)
MMMYYYY = [] #for collecting MonthYear for later use
t_int = [] #for collecting the respective TimeStepInterval used in the data files
t = 0 #initial timestep interval
    
while year <= <last year of data downloaded>: #update to include final year or last year desired for data
    x = [1,2,3,4,5,6,7,8,9,10,11,12] #months in a year
    for i in x:
        l = calendar.monthlen(year,i) #calculates number of days in a month (to include leap years)
        days.append(l)
        m = calendar.month_abbr[i] #generates text of month name
        y = str(year)
        n = str(m+y) #combines month name and year for later use
        MMMYYYY.append(n)
        t = t + (l*720) #calculates timestepinterval in dataname
        t_int.append(t)
    year +=1
    
MonthYear = pd.DataFrame({'MMMYYYY':MMMYYYY,'TimeStepInt':t_int})
MonthYear.info()

#create timestep module to determine timestepinterval for a specified MMMYYYY
def timestep(N):
    int1 = MonthYear.loc[MonthYear.MMMYYYY == N, 'TimeStepInt'].values[0]
    int1 = int(int1)
    return int1

#=============================================================================
# Reading in Data Files
#=============================================================================
#verify directory
os.chdir('your working directory')

#horizontal dimensions
XC=rdmds('XC'); XG=rdmds('XG');
YC=rdmds('YC'); YG=rdmds('YG');
#vertical dimensions
ZC=rdmds('RC'); ZG=rdmds('RF');
ZC=-np.squeeze(ZC);
ZG=-np.squeeze(ZG);

#Axis rotation factors
AngleSN=rdmds('AngleCS'); 
AngleCS=-rdmds('AngleSN');

# Read data file
tr123=rdmds('state_3d_set3',t); #for tracers

TSUVW=rdmds('state_3d_set2',t); #for velocities

U = TSUVW[2,:,:,:];
V = TSUVW[3,:,:,:];
W = TSUVW[4,:,:,:];

tr1 = tr123[0,:,:,:];
tr2 = tr123[1,:,:,:];
tr3 = tr123[2,:,:,:];

#=============================================================================
# Creating Geographic Bounds
#=============================================================================
#Land Mask for Amundsen sea
maskInC = rdmds('maskInC'); #1 = water, 0 = land
LandMask = maskInC.astype(bool)

#comment out if you want to view Amundsen AND Bellingshausen Sea (ABS) data
## Create masked arrays for XC and YC bound within the Amundsen Sea region
#AmundsenSeaLat = YC < -72 #greater in magnitude
#AmundsenSeaLon = XC < -98 #greater in magnitude

# Create masked arrays for XC and YC
XC_Amundsen = XC.copy()
XC_Amundsen[~(LandMask)] = np.nan
XC_Amundsen[~(AmundsenSeaLat)]= np.nan #comment out if you want to see ABS data
XC_Amundsen[~(AmundsenSeaLon)]= np.nan #comment out if you want to see ABS data
XC_Amundsen_bool = np.isnan(XC_Amundsen).astype(bool)
XC_Amundsen_doub = XC_Amundsen_bool.astype(float)
YC_Amundsen = YC.copy()
YC_Amundsen[~(LandMask)] = np.nan
YC_Amundsen[~(AmundsenSeaLat)]= np.nan #comment out if you want to see ABS data
YC_Amundsen[~(AmundsenSeaLon)]= np.nan #comment out if you want to see ABS data

#=============================================================================
# Plotting Concentration/Velocities Across Amundsen Sea at Various Depths 
# at Specified Time
#=============================================================================

#create depth list 
depth = np.arange(0,36,4)

#create subplot dimensions
a = 3  # number of rows
b = 3  # number of columns
c = 1  # initialize plot counter

#Tracer Plot
plt.figure(figsize = (15,8))
for i in depth:
    plt.subplot(a, b, c)
    plt.title(str(int(ZG[i])) +'m')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    i=plt.pcolor(XC_Amundsen,YC_Amundsen,tr1[i,:,:], vmin=0, vmax=1)
    c = c + 1
    plt.tight_layout()
plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
cax = plt.axes((0.85, 0.1, 0.075, 0.8))
plt.colorbar(cax=cax,label='Tracer Concentration ('+date+')')
plt.show()

#create subplot dimensions for second figure
d = 2  # number of rows
e = 4  # number of columns
f = 1  # initialize plot counter

#Vertical Velocity Plot
plt.figure(figsize = (15,7))
for i in depth:
    plt.subplot(d, e, f)
    plt.title(str(int(ZG[i])) +'m')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    i=plt.pcolor(XC_Amundsen,YC_Amundsen,W[i,:,:],vmin=-0.006, vmax=0.008)
    f = f + 1
    plt.tight_layout()
plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
cax = plt.axes((0.85, 0.1, 0.075, 0.8))
plt.colorbar(cax=cax,label='Vertical Velocities (m/s) ('+date+')')
plt.show()