import csv
import numpy as np
import pandas as pd

from configuration import *
from visualization import event_display
from reconstruction import reconstruct

import argparse
parser = argparse.ArgumentParser(description='analyze DT data')
parser.add_argument('-i', '--input',  help='The unpacked input file to analyze')
parser.add_argument("-v", "--verbose", default=False, action="store_true", help="increase output verbosity")
parser.add_argument("-e", "--visualize", default=False, action="store_true", help="show event display")
args = parser.parse_args()


# the base selections
def skip_event(selectedhits):
    skip = False
    # at least 3 chambers with hits
    if 3 not in selectedhits.chamber.unique() or len(selectedhits.chamber.unique())<3: skip=True
    # at least 2 hits in 2 different layers; not more than 10 hits per chamber
    for chamber in selectedhits.chamber.unique():
        if len(selectedhits[selectedhits.chamber==chamber].layer.unique()) < 3: skip=True
        if len(selectedhits[selectedhits.chamber==chamber].chamber.tolist()) > 7: skip=True
    return skip



with open("Run331.txt","r") as csvfile:
    reader=csv.reader(csvfile, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
    for event in reader:
        eventID=event[0]
        nhits=event[1]

        # not an empty event
        if nhits==0: continue
        
        # create table
        hits = [event[n:n+len(features)] for n in range(2, len(event), len(features))]
        allhits=pd.DataFrame(hits)
        allhits.columns = features
        allhits['xmean'] = (allhits.xleft+allhits.xright)/2

        # add global coordinates
        layer_conditions = [allhits.layer==1, allhits.layer==2, allhits.layer==3, allhits.layer==4]
        chamber_conditions = [allhits.chamber==0, allhits.chamber==1, allhits.chamber==2, allhits.chamber==3]
        allhits['globalz'] = np.select(layer_conditions, local_z_shifts, default=0) + np.select(chamber_conditions, global_z_shifts, default=0)
        allhits['globalxleft'] = -allhits['xleft'] + np.select(chamber_conditions, global_x_shifts, default=0)
        allhits['globalxright'] = -allhits['xright'] + np.select(chamber_conditions, global_x_shifts, default=0)
        allhits['globalxmean'] = -allhits['xmean'] + np.select(chamber_conditions, global_x_shifts, default=0)

        # select hits in range
        selectedhits_tmp = {}
        for chamber in ranges:
            selectedhits_tmp[chamber]=allhits.loc[(allhits.chamber==chamber) & (allhits.xmean>ranges[chamber][0]) & (allhits.xmean<ranges[chamber][1])]
        selectedhits = pd.concat(list(selectedhits_tmp.values()))

        # select only candidate events
        if skip_event(selectedhits): continue

        if args.verbose:
            print ("----")
            print (eventID)
            print (selectedhits)
            
        # reconstruct segments in each chamber
        segments = reconstruct(selectedhits, args.verbose)
            
        # visualize events    
        if args.visualize: event_display(eventID, allhits,selectedhits, segments)

            
            


        
