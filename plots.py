import numpy as np
import matplotlib.pyplot as plt

from configuration import *


class plotter():
    def __init__(self):
        self.deltaX = {'12at1':np.array([]),'12at2':np.array([]),'34at3':np.array([]),'34at4':np.array([])}
        self.phi = {'1':np.array([]),'2':np.array([]),'3':np.array([]),'4':np.array([])}
        self.deltaPhi = {'12':np.array([]),'34':np.array([])}

    def update(self, segments):
        try:
            if abs(segments[0].c[0])<0.2 and abs(segments[1].c[0])<0.2:
                self.deltaX['12at1']=np.append(self.deltaX['12at1'],segments[0](global_z_shifts[0]) - segments[1](global_z_shifts[0]))
                self.deltaX['12at2']=np.append(self.deltaX['12at2'],segments[0](global_z_shifts[1]) - segments[1](global_z_shifts[1]))
                self.phi['1']=np.append(self.phi['1'],segments[0].c[0])
                self.phi['2']=np.append(self.phi['2'],segments[1].c[0])
                self.deltaPhi['12']=np.append(self.deltaPhi['12'],segments[0].c[0]-segments[1].c[0])
        except: pass
        try:
            if abs(segments[2].c[0])<0.2 and abs(segments[3].c[0])<0.2:
                self.deltaX['34at3']=np.append(self.deltaX['34at3'],segments[2](global_z_shifts[0]) - segments[3](global_z_shifts[0]))
                self.deltaX['34at4']=np.append(self.deltaX['34at4'],segments[2](global_z_shifts[1]) - segments[3](global_z_shifts[1]))
                self.phi['3']=np.append(self.phi['3'],segments[2].c[0])
                self.phi['4']=np.append(self.phi['4'],segments[3].c[0])
                self.deltaPhi['34']=np.append(self.deltaPhi['34'],segments[2].c[0]-segments[3].c[0])
        except: pass
                
    def plot(self):
        figures = {"deltaX": plt.figure(num=1,figsize=(8,8)), "deltaPhi":plt.figure(num=2,figsize=(8,8))}
        axes = {"deltaX":[],"deltaPhi":[]}

        # Delta X
        axes["deltaX"].append(figures["deltaX"].add_subplot(2,1,1))
        axes["deltaX"].append(figures["deltaX"].add_subplot(2,1,2))
        for ax in axes["deltaX"]:
            ax.set_ylabel("entries")
            ax.set_xlabel("deltaX [mm]")
            ax.set_xlim(-100, 100)
        axes["deltaX"][0].set_title("At Chamber 1")
        axes["deltaX"][0].hist(self.deltaX['12at1'], 100)
        axes["deltaX"][1].set_title("At Chamber 2")
        axes["deltaX"][1].hist(self.deltaX['12at2'], 100)
        plt.tight_layout()
        
        # Phi and Delta Phi
        axes["deltaPhi"].append(figures["deltaPhi"].add_subplot(2,1,1))
        axes["deltaPhi"][0].set_ylabel("phi 1 [rad]")
        axes["deltaPhi"][0].set_xlabel("phi 2 [rad]")
        axes["deltaPhi"][0].scatter(self.phi['1'],self.phi['2'])
        
        axes["deltaPhi"].append(figures["deltaPhi"].add_subplot(2,1,2))
        axes["deltaPhi"][1].set_ylabel("entries")
        axes["deltaPhi"][1].set_xlabel("delta phi")
        axes["deltaPhi"][1].set_xlim(-0.2, 0.2)
        axes["deltaPhi"][1].hist(self.deltaPhi['12'], 200)
        
        plt.tight_layout()
        plt.show()
        
    def printout(self):
        print ("--- S T A T I S T I C A L   S U M M A R Y ---")
        print ("Delta X Ch1-Ch2 at Ch1: mean =", self.deltaX['12at1'].mean(), " RMS = ", self.deltaX['12at1'].std())
        print ("Delta X Ch1-Ch2 at Ch2: mean =", self.deltaX['12at2'].mean(), " RMS = ", self.deltaX['12at2'].std())
        print ("Delta X Ch3-Ch4 at Ch3: mean =", self.deltaX['34at3'].mean(), " RMS = ", self.deltaX['34at3'].std())
        print ("Delta X Ch4-Ch4 at Ch4: mean =", self.deltaX['34at4'].mean(), " RMS = ", self.deltaX['34at4'].std())
        for i in range(1,5): print ("Phi",i,": mean = ",self.phi[str(i)].mean()," RMS = ", self.phi[str(i)].std())
        print ("Delta Phi Ch1-Ch2: mean =", self.deltaPhi['12'].mean(), " RMS = ", self.deltaPhi['12'].std())
        print ("Delta Phi Ch3-Ch4: mean =", self.deltaPhi['34'].mean(), " RMS = ", self.deltaPhi['34'].std())
