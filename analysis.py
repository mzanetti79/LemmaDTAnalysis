import csv
import numpy as np
import pandas as pd

from configuration import *
from visualization import event_display
from reconstruction import segment_reconstructor, track_reconstructor
from plots import plotter
from calibration import calibrator
from residuals import residuals_estimator

import argparse
parser = argparse.ArgumentParser(description='analyze DT data')
parser.add_argument('-i', '--input',  help='The unpacked input file to analyze')
parser.add_argument("-v", "--verbose", default=False, action="store_true", help="increase output verbosity")
parser.add_argument("-e", "--visualize", default=False, action="store_true", help="show event display")
parser.add_argument("-c", "--calibration", default=False, action="store_true", help="for calibration runs")
parser.add_argument("-t", "--timeboxes", default=False, action="store_true", help="compute timeboxes")
parser.add_argument("-r", "--residuals", default=False, action="store_true", help="compute residuals")
parser.add_argument("-N", "--num_events", default=-1, type=int, help="lines to be processed")
args = parser.parse_args()

# the base selections
def skip_event(selectedhits, calibration):
    skip = False
    chambers = selectedhits.chamber.unique()
    if calibration:
        if (not all(x in chambers for x in [0, 1])) and (not all(x in chambers for x in [2, 3])): skip=True
    else:
        if 3 not in chambers or len(chambers)<3: skip=True
    for chamber in chambers:
        if len(selectedhits[selectedhits.chamber==chamber].layer.unique()) < 3: skip=True
        if len(selectedhits[selectedhits.chamber==chamber].chamber.tolist()) > 7: skip=True
    return skip


# Analyze the input file
with open(args.input,"r") as csvfile:
    # the plotter
    plotter = plotter()

    # the calibrator
    calibrator = calibrator()

    # the residual estimator
    estimator = residuals_estimator()
    
    # read the preporcessed csv file
    reader=csv.reader(csvfile, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
    counter=0
    for event in reader:
        counter+=1

        if counter%100==0: print (counter, "lines processed")
        if args.num_events>0 and counter>=args.num_events: break
            
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
        layer_conditions = [allhits.layer==4, allhits.layer==3, allhits.layer==2, allhits.layer==1]
        chamber_conditions = [allhits.chamber==0, allhits.chamber==1, allhits.chamber==2, allhits.chamber==3]
        allhits['globalz'] = np.select(layer_conditions, local_z_shifts, default=0) + np.select(chamber_conditions, global_z_shifts, default=0)

        correction = VDRIFT*TTRIGCORR["calibration"] if args.calibration else VDRIFT*TTRIGCORR["signal"] 
        allhits['globalxleft']  = -(allhits['xleft']-correction) + np.select(chamber_conditions, global_x_shifts, default=0)
        allhits['globalxright'] = -(allhits['xright']+correction) + np.select(chamber_conditions, global_x_shifts, default=0)
        allhits['globalxmean']  = -allhits['xmean'] + np.select(chamber_conditions, global_x_shifts, default=0)

        # select hits in range
        selectedhits_tmp = {}
        ranges = hit_ranges["calibration"] if args.calibration else hit_ranges["signal"]
        for chamber in ranges:
            selectedhits_tmp[chamber]=allhits.loc[(allhits.chamber==chamber) & (allhits.xmean>ranges[chamber][0]) & (allhits.xmean<ranges[chamber][1])]
        selectedhits = pd.concat(list(selectedhits_tmp.values()))

        # select only candidate events
        if skip_event(selectedhits, args.calibration): continue

        if args.verbose:
            print ("----")
            print (eventID)
            print (selectedhits)
            
        # reconstruct segments in each chamber
        segments, besthits = segment_reconstructor(selectedhits, args.verbose)
        tracks = track_reconstructor(besthits)
        # fill plots
        plotter.update(segments, tracks)
        # visualize events    
        if args.visualize: event_display(eventID, allhits,selectedhits, segments, tracks)
        # fill timeboxes
        if args.timeboxes: calibrator.update(selectedhits)
        # fill residuals
        if args.residuals: estimator.compute(selectedhits, besthits, segments)
            
    # stats
    plotter.printout()
    # plotting
    # plotter.plot()
    # timeboxes
    if args.timeboxes:
        calibrator.plot()
        calibrator.save()
    # residuals
    if args.residuals: estimator.save()
