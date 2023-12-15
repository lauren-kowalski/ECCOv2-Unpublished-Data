#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 13:40:18 2023

@author: laurenkowalski
"""

#import glob
#filenames = sorted(glob.glob('/Users/laurenkowalski/Desktop/WestAntarcticaDocs/Data/Yoshi_Model/Testing2023/state_3d_set3.0000*.data'))
#print(filenames)
import numpy as np
import matplotlib.pyplot as plt
from MITgcmutils import rdmds
import pandas as pd
import os
import calendar

os.chdir('your working directory')

#=============================================================================
# Define Time Step Module
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
    
while year <= <last year of datadownloaded>: #update to include final year or last year desired for data
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
# Define Geographic Boundary
#=============================================================================

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

#Land Mask for Amundsen sea
maskInC = rdmds('maskInC'); #1 = water, 0 = land
LandMask = maskInC.astype(bool)

#comment out if you want to view Amundsen AND Bellingshausen Sea (ABS) data
# Create masked arrays for XC and YC bound within the Amundsen Sea region
AmundsenSeaLat = YC < -72 #greater in magnitude
AmundsenSeaLon = XC < -98 #greater in magnitude

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
# Plot Annual Data (Tracer Concentration) at Specified Depth
#=============================================================================

#Plotting Yearly Data @ Depth Step 
#state_3d_set3 = Tracer Data
#3x4 subplots that share all axes
fig, axs = plt.subplots(3, 4, sharex='all', sharey='all') 
year = '05'
d = 19 #Depth Step - see  .xlsx for actual depth step / depth correlation

#January
#Tracer []s
jan = (timestep('jan'+year))
jan_tr123=rdmds('state_3d_set3',jan);
jan_tr1 = jan_tr123[0,:,:,:];
jan_tr2 = jan_tr123[1,:,:,:];
jan_tr3 = jan_tr123[2,:,:,:];
axs[0,0].pcolor(XC_Amundsen,YC_Amundsen,jan_tr1[d,:,:])
axs[0,0].set_title('January')

#February
#Tracer []s
feb = (timestep('feb'+year))
feb_tr123=rdmds('state_3d_set3',feb);
feb_tr1 = feb_tr123[0,:,:,:];
feb_tr2 = feb_tr123[1,:,:,:];
feb_tr3 = feb_tr123[2,:,:,:];
axs[0,1].pcolor(XC_Amundsen,YC_Amundsen,feb_tr1[d,:,:])
axs[0,1].set_title('February')

#March
#Tracer []s
mar = (timestep('mar'+year))
mar_tr123=rdmds('state_3d_set3',mar);
mar_tr1 = mar_tr123[0,:,:,:];
mar_tr2 = mar_tr123[1,:,:,:];
mar_tr3 = mar_tr123[2,:,:,:];
axs[0,2].pcolor(XC_Amundsen,YC_Amundsen,mar_tr1[d,:,:])
axs[0,2].set_title('March')

#April
#Tracer []s
apr = (timestep('apr'+year))
apr_tr123=rdmds('state_3d_set3',apr);
apr_tr1 = apr_tr123[0,:,:,:];
apr_tr2 = apr_tr123[1,:,:,:];
apr_tr3 = apr_tr123[2,:,:,:];
axs[0,3].pcolor(XC_Amundsen,YC_Amundsen,apr_tr1[d,:,:])
axs[0,3].set_title('April')

#May
#Tracer []s
may = (timestep('may'+year))
may_tr123=rdmds('state_3d_set3',may);
may_tr1 = may_tr123[0,:,:,:];
may_tr2 = may_tr123[1,:,:,:];
may_tr3 = may_tr123[2,:,:,:];
axs[1,0].pcolor(XC_Amundsen,YC_Amundsen,may_tr1[d,:,:])
axs[1,0].set_title('May')

#June
#Tracer []s
jun = (timestep('jun'+year))
jun_tr123=rdmds('state_3d_set3',jun);
jun_tr1 = jun_tr123[0,:,:,:];
jun_tr2 = jun_tr123[1,:,:,:];
jun_tr3 = jun_tr123[2,:,:,:];
axs[1,1].pcolor(XC_Amundsen,YC_Amundsen,jun_tr1[d,:,:])
axs[1,1].set_title('June')

#July
#Tracer []s
jul = (timestep('jul'+year))
jul_tr123=rdmds('state_3d_set3',jul);
jul_tr1 = jul_tr123[0,:,:,:];
jul_tr2 = jul_tr123[1,:,:,:];
jul_tr3 = jul_tr123[2,:,:,:];
axs[1,2].pcolor(XC_Amundsen,YC_Amundsen,jul_tr1[d,:,:])
axs[1,2].set_title('July')

#August
#Tracer []s
aug = (timestep('aug'+year))
aug_tr123=rdmds('state_3d_set3',aug);
aug_tr1 = aug_tr123[0,:,:,:];
aug_tr2 = aug_tr123[1,:,:,:];
aug_tr3 = aug_tr123[2,:,:,:];
axs[1,3].pcolor(XC_Amundsen,YC_Amundsen,aug_tr1[d,:,:])
axs[1,3].set_title('August')

#September
#Tracer []s
sep = (timestep('sep'+year))
sep_tr123=rdmds('state_3d_set3',sep);
sep_tr1 = sep_tr123[0,:,:,:];
sep_tr2 = sep_tr123[1,:,:,:];
sep_tr3 = sep_tr123[2,:,:,:];
axs[2,0].pcolor(XC_Amundsen,YC_Amundsen,sep_tr1[d,:,:])
axs[2,0].set_title('September')

#October
#Tracer []s
oct_t = (timestep('oct'+year))
oct_tr123=rdmds('state_3d_set3',oct_t);
oct_tr1 = oct_tr123[0,:,:,:];
oct_tr2 = oct_tr123[1,:,:,:];
oct_tr3 = oct_tr123[2,:,:,:];
axs[2,1].pcolor(XC_Amundsen,YC_Amundsen,oct_tr1[d,:,:])
axs[2,1].set_title('October')

#November
#Tracer []s
nov = (timestep('nov'+year))
nov_tr123=rdmds('state_3d_set3',nov);
nov_tr1 = nov_tr123[0,:,:,:];
nov_tr2 = nov_tr123[1,:,:,:];
nov_tr3 = nov_tr123[2,:,:,:];
axs[2,2].pcolor(XC_Amundsen,YC_Amundsen,nov_tr1[d,:,:])
axs[2,2].set_title('November')

#December
#Tracer []s
dec = (timestep('dec'+year))
dec_tr123=rdmds('state_3d_set3',dec);
dec_tr1 = dec_tr123[0,:,:,:];
dec_tr2 = dec_tr123[1,:,:,:];
dec_tr3 = dec_tr123[2,:,:,:];
axs[2,3].pcolor(XC_Amundsen,YC_Amundsen,dec_tr1[d,:,:])
axs[2,3].set_title('December')
#
fig.suptitle('Tracer Concentration - '+year+' Seasonal Cycle @ '+str(int(ZG[d]))+'m')
#plt.savefig('your working directory/TR1_'+year+'_SeasonalCycle_'+str(int(ZG[d]))+'m.jpg')

#=============================================================================
# Plot Annual Data (Vertical Velocity) at Specified Depth
#=============================================================================

#state_3d_set2 = Temp/Salinity/Velocity Data
#Plotting Yearly Data @ Depth Step 
fig, axs = plt.subplots(3, 4, sharex='all', sharey='all') #3x4 subplots that share all axes

#January
#Velocities
jan = (timestep('jan'+year))
jan_TSUVW=rdmds('state_3d_set2',jan);
jan_U = jan_TSUVW[2,:,:,:];
jan_V = jan_TSUVW[3,:,:,:];
jan_W = jan_TSUVW[4,:,:,:];
axs[0,0].pcolor(XC_Amundsen,YC_Amundsen,jan_W[d,:,:])
axs[0,0].set_title('January')

#February
#Velocities
feb = (timestep('feb'+year))
feb_TSUVW=rdmds('state_3d_set2',feb);
feb_U = feb_TSUVW[2,:,:,:];
feb_V = feb_TSUVW[3,:,:,:];
feb_W = feb_TSUVW[4,:,:,:];
axs[0,1].pcolor(XC_Amundsen,YC_Amundsen,feb_W[d,:,:])
axs[0,1].set_title('February')

#March
#Velocities
mar = (timestep('mar'+year))
mar_TSUVW=rdmds('state_3d_set2',mar);
mar_U = mar_TSUVW[2,:,:,:];
mar_V = mar_TSUVW[3,:,:,:];
mar_W = mar_TSUVW[4,:,:,:];
axs[0,2].pcolor(XC_Amundsen,YC_Amundsen,mar_W[d,:,:])
axs[0,2].set_title('March')

#April
#Velocities
apr = (timestep('apr'+year))
apr_TSUVW=rdmds('state_3d_set2',apr);
apr_U = apr_TSUVW[2,:,:,:];
apr_V = apr_TSUVW[3,:,:,:];
apr_W = apr_TSUVW[4,:,:,:];
axs[0,3].pcolor(XC_Amundsen,YC_Amundsen,apr_W[d,:,:])
axs[0,3].set_title('April')

#May
#Velocities
may = (timestep('may'+year))
may_TSUVW=rdmds('state_3d_set2',may);
may_U = may_TSUVW[2,:,:,:];
may_V = may_TSUVW[3,:,:,:];
may_W = may_TSUVW[4,:,:,:];
axs[1,0].pcolor(XC_Amundsen,YC_Amundsen,may_W[d,:,:])
axs[1,0].set_title('May')

#June
#Velocities
jun = (timestep('jun'+year))
jun_TSUVW=rdmds('state_3d_set2',jun);
jun_U = jun_TSUVW[2,:,:,:];
jun_V = jun_TSUVW[3,:,:,:];
jun_W = jun_TSUVW[4,:,:,:];
axs[1,1].pcolor(XC_Amundsen,YC_Amundsen,jun_W[d,:,:])
axs[1,1].set_title('June')

#July
#Velocities
jul = (timestep('jul'+year))
jul_TSUVW=rdmds('state_3d_set2',jul);
jul_U = jul_TSUVW[2,:,:,:];
jul_V = jul_TSUVW[3,:,:,:];
jul_W = jul_TSUVW[4,:,:,:];
axs[1,2].pcolor(XC_Amundsen,YC_Amundsen,jul_W[d,:,:])
axs[1,2].set_title('July')

#August
#Velocities
aug = (timestep('aug'+year))
aug_TSUVW=rdmds('state_3d_set2',aug);
aug_U = aug_TSUVW[2,:,:,:];
aug_V = aug_TSUVW[3,:,:,:];
aug_W = aug_TSUVW[4,:,:,:];
axs[1,3].pcolor(XC_Amundsen,YC_Amundsen,aug_W[d,:,:])
axs[1,3].set_title('August')

#September
#Velocities
sep = (timestep('sep'+year))
sep_TSUVW=rdmds('state_3d_set2',sep);
sep_U = sep_TSUVW[2,:,:,:];
sep_V = sep_TSUVW[3,:,:,:];
sep_W = sep_TSUVW[4,:,:,:];
axs[2,0].pcolor(XC_Amundsen,YC_Amundsen,sep_W[d,:,:])
axs[2,0].set_title('September')

#October
#Velocities
oct_t = (timestep('oct'+year))
oct_TSUVW=rdmds('state_3d_set2',oct_t);
oct_U = oct_TSUVW[2,:,:,:];
oct_V = oct_TSUVW[3,:,:,:];
oct_W = oct_TSUVW[4,:,:,:];
axs[2,1].pcolor(XC_Amundsen,YC_Amundsen,oct_W[d,:,:])
axs[2,1].set_title('October')

#November
#Velocities
nov = (timestep('nov'+year))
nov_TSUVW=rdmds('state_3d_set2',nov);
nov_U = nov_TSUVW[2,:,:,:];
nov_V = nov_TSUVW[3,:,:,:];
nov_W = nov_TSUVW[4,:,:,:];
axs[2,2].pcolor(XC_Amundsen,YC_Amundsen,nov_W[d,:,:])
axs[2,2].set_title('November')

#December
#Velocities
dec = (timestep('dec'+year))
dec_TSUVW=rdmds('state_3d_set2',dec);
dec_U = dec_TSUVW[2,:,:,:];
dec_V = dec_TSUVW[3,:,:,:];
dec_W = dec_TSUVW[4,:,:,:];
axs[2,3].pcolor(XC_Amundsen,YC_Amundsen,dec_W[d,:,:])
axs[2,3].set_title('December')
#
fig.suptitle('Wvel - '+year+' Seasonal Cycle @ '+str(int(ZG[d]))+'m')
#plt.savefig('your working directory/Wvel_'+year+'_SeasonalCycle_'+str(int(ZG[d]))+'m.jpg')