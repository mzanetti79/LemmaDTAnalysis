import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from configuration import *

def event_display(eventID, allhits, selectedhits, segments, tracks):

    fig, ax = plt.subplots(figsize=(10,7))
    # set figure propreties
    ax.set_xlim([-1000,1000])
    ax.set_ylim([-100,1000])

    # draw hits
    ax1 = allhits.plot.scatter(x='globalxleft',y='globalz',c='Green', ax=ax)
    ax2 = allhits.plot.scatter(x='globalxright',y='globalz',c='Green', ax=ax)
    ax3 = selectedhits.plot.scatter(x='globalxright',y='globalz',c='DarkBlue', ax=ax)
    ax4 = selectedhits.plot.scatter(x='globalxleft',y='globalz',c='Red', ax=ax)
    
    # draw chamber boxes
    chamber_boxes = [patches.Rectangle(coordinates,-XCELL*17,ZCELL*4,linewidth=1,edgecolor='#d3d3d3', facecolor="none")
                         for coordinates in list(zip([xs for xs in global_x_shifts],[zs-ZCELL/2 for zs in global_z_shifts]))]
    for chamber_box in chamber_boxes: ax.add_patch(chamber_box)

    # draw cells
    for index, hit in selectedhits.iterrows():
        ax.add_patch(patches.Rectangle((hit["globalxmean"]-XCELL/2,hit["globalz"]-ZCELL/2),XCELL,ZCELL,linewidth=1,edgecolor='#d3d3d3', facecolor="none"))

    # draw segments
    yi = np.linspace(-20, 900, 1000)
    for chamber in segments: ax.plot(segments[chamber](yi), yi, "c", linestyle='--')

    # draw tracks
    for leg in tracks: ax.plot(tracks[leg](yi), yi,"k-")
    
    plt.xlabel("x [mm]")
    plt.ylabel("z [mm]")        
    plt.title("Event "+str(int(eventID)))
    plt.show()

    
