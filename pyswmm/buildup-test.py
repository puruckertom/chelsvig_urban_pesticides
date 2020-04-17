# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 12:42:22 2017

@author: KRatliff
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

from pyswmm import Simulation, Subcatchments, Nodes

SC1_buildup = np.array([])
SC2_buildup = np.array([])
SC3_buildup = np.array([])
outfall_buildup = np.array([])
time = np.array([])


with Simulation('buildup-test.inp') as sim:

    subcatch_object = Subcatchments(sim)
    Out1 = Nodes(sim)["Out1"]
    
    SC1 = subcatch_object["S1"]
    SC2 = subcatch_object["S2"]
    SC3 = subcatch_object["S3"]
    print(SC1.area)
    print(SC1.subcatchmentid)
    
    for step in sim:
        SC1_buildup = np.append(SC1_buildup, SC1.statistics['pollutant_buildup']['test-pollutant']*SC1.area)
        SC2_buildup = np.append(SC2_buildup, SC2.statistics['pollutant_buildup']['test-pollutant']*SC2.area)
        SC3_buildup = np.append(SC3_buildup, SC3.statistics['pollutant_buildup']['test-pollutant']*SC3.area)
        outfall_buildup = np.append(outfall_buildup, Out1.outfall_statistics['pollutant_loading']['test-pollutant'])
        time = np.append(time, sim.current_time)
        pass

    print(Out1.outfall_statistics)
    
    #np.savetxt('SC1_buildup.out', SC1_buildup, fmt='%.6f', newline=os.linesep)
    #np.savetxt('SC2_buildup.out', SC2_buildup, fmt='%.6f', newline=os.linesep)
    #np.savetxt('SC3_buildup.out', SC3_buildup, fmt='%.6f', newline=os.linesep)
    #np.savetxt('outfall_loading.out', outfall_buildup, fmt='%.6f', newline=os.linesep)
    
    f = plt.figure()
    SC1, = plt.plot(time, SC1_buildup)
    SC2, = plt.plot(time, SC2_buildup)
    SC3, = plt.plot(time, SC3_buildup)
    plt.legend([SC1, SC2, SC3], ['Subcatchment 1','Subcatchment 2','Subcatchment 3'])
    plt.gcf().autofmt_xdate()
    plt.title('Subcatchment Surface Contamination')
    plt.xlabel('time')
    plt.ylabel('hypothetical contaminant loading (CFU/ac)')
    plt.savefig('sc_buildups.png', dpi=300)
    plt.close(f)
    
    f = plt.figure(figsize=(7,3))
    plt.plot(time, outfall_buildup)
    plt.title('cumulative outfall contamination')
    plt.ylabel('concentration (#/L)')
    plt.xlabel('time')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig('outfall_loading.png', dpi=300)
    plt.close(f)
    
    sim.report()