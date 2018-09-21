# basic features in original data
features = ["chamber","layer","xleft","xright","timens"]

# global ranges for the signal hits
hit_ranges = {"signal":{0:[540.,720.],1:[540.,720],2:[0.,200.],3:[0.,200.]},
              "calibration":{0:[0.,720.],1:[0.,720],2:[0.,720.],3:[0.,720.]}}

# chamber basic dimensions
XCELL = 42.
ZCELL = 13.
VDRIFT = 0.05385
#TTRIGCORR = {"signal":10,"calibration":2}
TTRIGCORR = {"signal":0,"calibration":0}
# global X shifts
global_x_shifts = [994.2, 947.4,-267.4,-261.5,]

# global Z translations
chamber_z_offset = 770. + ZCELL*4 +1.5
global_z_shifts = [chamber_z_offset, 0, chamber_z_offset,0]
local_z_shifts = [z*ZCELL for z  in range(0,4)]
