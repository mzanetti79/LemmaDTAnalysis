
# basic features in original data
features = ["chamber","layer","xleft","xright","timens"]

# global ranges for the signal hits
ranges = {0:[540.,720.],1:[540.,720],2:[0.,200.],3:[0.,200.]}
#ranges = {0:[0.,720.],1:[0.,720],2:[0.,720.],3:[0.,720.]}

# chamber basic dimensions
XCELL = 42.
ZCELL = 13.
VDRIFT = 0.05385

# global X translations
#X0 = 960
#chamber_x_offset = -(737+472.5+10.)
#chamber0_extra_x_offset = 40.
#global_x_shifts = [X0+chamber0_extra_x_offset, X0, X0+chamber_x_offset, X0+chamber_x_offset]


X0 = 950.1-24.2 # from geometry: arbitrary in DT system, roughly corresponding to beam position 
led_position_wrt_first_wire = 0 # arbitrary in DT system, to be assigned in order to move to global coordinates
X0+=led_position_wrt_first_wire

x_offset_between_right_chambers = 47.0 # shift of chamber 1 w.r.t 2 (averaged from Saleve and Jura)
x_offset_between_left_chambers = -6.4 # shift of chamber 3 w.r.t 4
x_offset_between_front_chambers = - 1206.3 # distance between 2 and 4 (averaged from Saleve and Jura)

global_x_shifts = [
    X0+x_offset_between_right_chambers, # chamber 1, shifted by 47
    X0, # chamber 2, the reference
    X0+x_offset_between_front_chambers+x_offset_between_left_chambers, # chamber 3, shifted by -6.4 w.r.t chamber 4
    X0+x_offset_between_front_chambers, # chamber 4, the reference on the left
    ]

# global Z translations
chamber_z_offset = 770. + ZCELL*4 +1.5
global_z_shifts = [chamber_z_offset, 0, chamber_z_offset,0]
local_z_shifts = [z*ZCELL for z  in range(0,4)]
