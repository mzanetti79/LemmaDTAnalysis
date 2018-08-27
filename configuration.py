
# basic features in original data
features = ["chamber","layer","xleft","xright","timens"]

# global ranges for the signal hits
ranges = {0:[540.,720.],1:[540.,720],2:[0.,200.],3:[0.,200.]}

# chamber basic dimensions
XCELL = 42.
ZCELL = 13.

# global X translations
X0 = 960
chamber_x_offset = -(737+472.5+10.)
chamber0_extra_x_offset = 40.
global_x_shifts = [X0+chamber0_extra_x_offset, X0, X0+chamber_x_offset, X0+chamber_x_offset]

# global Z translations
chamber_z_offset = 770. + ZCELL*4 +1.5
global_z_shifts = [chamber_z_offset, 0, chamber_z_offset,0]
local_z_shifts = [z*ZCELL for z  in range(0,4)]
