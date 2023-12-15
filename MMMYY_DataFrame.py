#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 11:23:38 2023

@author: laurenkowalski
"""

import calendar
import pandas as pd

#define start year of data
year = 1992

#create empty lists for appending...
days = [] #for number of days in a month (to include leap years)
MMMYYYY = [] #for collecting MonthYear for later use
t_int = [] #for collecting the respective TimeStepInterval used in the data files
t = 0 #initial timestep interval
    
while year <= 1994: #update to include final year or last year desired for data
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

