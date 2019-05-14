# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 12:04:45 2018

@author: footb
"""

import pyomo
import pandas as pd
import numpy
from numpy import genfromtxt
import os

os.getcwd()
os.chdir("/Users/footb/Desktop/Misc/Work/ATAK")


###################################  read data from text files  ##############################################################
##have the h dataframe saved as h_lower and h_upper (demand at node i for scenario k) 
##and d dataframe saved as d_lower and d_upper(snr at i from j during scenario k)
##new dataframes C and F (C = antenna site j is a necessary antenna site, F = antenna site j is a feasible antenna site)


h_lower = pd.read_csv('h_lower.txt', sep=",", header = 0, index_col = 0)
h_upper = pd.read_csv('h_upper.txt', sep=",", header = 0, index_col = 0)
d = pd.read_csv('d.txt', sep=",", header = 0, index_col = 0)
m = pd.read_csv('m.txt', sep=",", header = None, index_col = 0)
q = pd.read_csv('q.txt', sep = ",", header = None, index_col = 0)
Vhat = pd.read_csv('Vhat.txt', sep = ",", header = None, index_col = 0)
C = pd.read_csv('C.txt', sep = ",", header = 0, index_col = 0)
F_lat = pd.read_csv('F_lat.txt', sep = ",", header = None, index_col = 0)
F_long = pd.read_csv('F_long.txt', sep = ",", header = 0, index_col = 0)

###Given by dimensions of data frame, not needed to be inputted
i = h_lower.shape[1]*h_upper.shape[0] # demand nodes
j = F_lat.shape[0] # antenna placement possibilities
k = 10 # scenarios (given)

######################################  Generate scenarios of the demand, snr  #################################################
h_lower = h_lower.values
h_lower_ik = h_lower.flatten() # turns the 3x3 matrix into a 9x1 array
h_upper = h_upper.values
h_upper_ik = h_upper.flatten() # turns the 3x3 matrix into a 9x1 array

h = numpy.zeros(shape = [h_lower_ik.shape[0],k]) # creates empty array to be filled by scenarios

## loop to create hik
count1 = 0
count2 = 0
for count1 in range(k):
    for count2 in range(i):
        h[count2, count1] = numpy.random.randint(low = h_lower_ik[count2], high = h_upper_ik[count2])


## Need to take the data input (lat, long, feasible antenna) and convert it into something that I can use (ijk)
        
# Take lat, long matrices for valid data points, put them into something I can use (feasible data points)

nw_corner_lat = 0
nw_corner_long = 0
se_corner_lat = 10
se_corner_long = 10
granularity = 1

i_F = F_lat.shape[0]
count1 = 0
count2 = 0


## F table is now what j is associated with what lat long, make it much easier to establish the points
F = numpy.zeros(shape = [F_lat.shape[0], 3])
#F.dtype.names = ('j', 'lat', 'long')
for count1 in range(i_F):
    F[count1, 0] = count2
    F[count1, 1] = F_lat[count2]
    F[count1, 2] = F_long[count2]
    count2 = count2 + 1


## Now want to turn the (lat, long) x k array into demand x supply
#d = d.values
#d_ik = d.flatten()













#Need to convert from grid to i and j
##h
d = d.values
d = d.flatten()

#turns datafile into numpy in order to stack 3d
d = d.values
#d = numpy.stack((dlower,dupper)) #just going to use the lower bound for SNR so we do not have to deal with uncertainty
