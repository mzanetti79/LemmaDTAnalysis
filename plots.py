import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from configuration import *


class plotter():
    def __init__(self):
        self.X = {'1':np.array([]),'2':np.array([]),'3':np.array([]),'4':np.array([])}
        self.phi = {'1':np.array([]),'2':np.array([]),'3':np.array([]),'4':np.array([])}
        self.Xc = {'1':np.array([]),'2':np.array([]),'3':np.array([]),'4':np.array([])}
        self.phic = {'1':np.array([]),'2':np.array([]),'3':np.array([]),'4':np.array([])}
        self.deltaX = {'12at1':np.array([]),'12at2':np.array([]),'34at3':np.array([]),'34at4':np.array([])}
        self.deltaPhi = {'12':np.array([]),'34':np.array([])}
        self.trackPhi = {'neg':np.array([]),'pos':np.array([])}
        self.trackX = {'neg':np.array([]),'pos':np.array([])}
        self.eventTracksPhi = {'neg':np.array([]),'pos':np.array([])}
        self.eventTracksX = {'neg':np.array([]),'pos':np.array([])}
                
    def update(self, segments, tracks):

        for i in segments.keys():
            if abs(segments[i].c[0])<0.2:
                self.X[str(int(i+1))]=np.append(self.X[str(int(i+1))],segments[i](global_z_shifts[int(i%2)]))
                self.phi[str(int(i+1))]=np.append(self.phi[str(int(i+1))],segments[i].c[0])

        if all(x in segments for x in [0, 1]):
            if abs(segments[0].c[0])<0.2 and abs(segments[1].c[0])<0.2:
                self.deltaX['12at1']=np.append(self.deltaX['12at1'],segments[0](global_z_shifts[0]) - segments[1](global_z_shifts[0]))
                self.deltaX['12at2']=np.append(self.deltaX['12at2'],segments[0](global_z_shifts[1]) - segments[1](global_z_shifts[1]))
                self.deltaPhi['12']=np.append(self.deltaPhi['12'],segments[0].c[0]-segments[1].c[0])
                self.phic['1']=np.append(self.phic['1'],segments[0].c[0])
                self.phic['2']=np.append(self.phic['2'],segments[1].c[0])
                self.Xc['1']=np.append(self.Xc['1'],segments[0](global_z_shifts[0]))
                self.Xc['2']=np.append(self.Xc['2'],segments[1](global_z_shifts[1]))
                                
        if all(x in segments for x in [2, 3]):
            if abs(segments[2].c[0])<0.2 and abs(segments[3].c[0])<0.2:
                self.deltaX['34at3']=np.append(self.deltaX['34at3'],segments[2](global_z_shifts[0]) - segments[3](global_z_shifts[0]))
                self.deltaX['34at4']=np.append(self.deltaX['34at4'],segments[2](global_z_shifts[1]) - segments[3](global_z_shifts[1]))
                self.deltaPhi['34']=np.append(self.deltaPhi['34'],segments[2].c[0]-segments[3].c[0])
                self.phic['3']=np.append(self.phic['3'],segments[2].c[0])
                self.phic['4']=np.append(self.phic['4'],segments[3].c[0])
                self.Xc['3']=np.append(self.Xc['3'],segments[2](global_z_shifts[0]))
                self.Xc['4']=np.append(self.Xc['4'],segments[3](global_z_shifts[1]))

        for leg in tracks.keys():
            self.trackPhi[leg]=np.append(self.trackPhi[leg], tracks[leg].c[0])
            self.trackX[leg]=np.append(self.trackX[leg], tracks[leg](global_z_shifts[0]))

        if all(leg in tracks for leg in ['neg', 'pos']):
            self.eventTracksPhi['pos']=np.append(self.eventTracksPhi['pos'], tracks['pos'].c[0])
            self.eventTracksX['pos']=np.append(self.eventTracksX['pos'], tracks['pos'](global_z_shifts[0]))
            self.eventTracksPhi['neg']=np.append(self.eventTracksPhi['neg'], tracks['neg'].c[0])
            self.eventTracksX['neg']=np.append(self.eventTracksX['neg'], tracks['neg'](global_z_shifts[0]))


    def plot(self):
        figures = {"deltaX": plt.figure(num=1,figsize=(10,8)), "deltaPhi":plt.figure(num=2,figsize=(10,8))}
        axes = {"deltaX":[],"deltaPhi":[]}
        
        # Delta X
        axes["deltaX"].append(figures["deltaX"].add_subplot(2,2,1))
        axes["deltaX"].append(figures["deltaX"].add_subplot(2,2,2))
        axes["deltaX"].append(figures["deltaX"].add_subplot(2,2,3))
        axes["deltaX"].append(figures["deltaX"].add_subplot(2,2,4))
        for ax in axes["deltaX"]:
            ax.set_ylabel("entries")
            ax.set_xlabel("deltaX [mm]")
            ax.set_xlim(-100, 100)
        axes["deltaX"][0].set_title("At Chamber 1")
        axes["deltaX"][0].hist(self.deltaX['12at1'], 200, normed=True)
        axes["deltaX"][1].set_title("At Chamber 2")
        axes["deltaX"][1].hist(self.deltaX['12at2'], 200, normed=True)
        axes["deltaX"][2].set_title("At Chamber 3")
        axes["deltaX"][2].hist(self.deltaX['34at3'], 100, normed=True)
        axes["deltaX"][3].set_title("At Chamber 4")
        axes["deltaX"][3].hist(self.deltaX['34at4'], 100, normed=True)
        
        # Phi and Delta Phi
        axes["deltaPhi"].append(figures["deltaPhi"].add_subplot(2,2,1))
        axes["deltaPhi"][0].set_ylabel("phi 1 [rad]")
        axes["deltaPhi"][0].set_xlabel("phi 2 [rad]")
        axes["deltaPhi"][0].scatter(self.phi['1'],self.phi['2'])
        axes["deltaPhi"].append(figures["deltaPhi"].add_subplot(2,2,2))
        axes["deltaPhi"][1].set_ylabel("entries")
        axes["deltaPhi"][1].set_xlabel("delta phi")
        axes["deltaPhi"][1].set_xlim(-0.2, 0.2)
        axes["deltaPhi"][1].hist(self.deltaPhi['12'], 200, normed=True)
        
        axes["deltaPhi"].append(figures["deltaPhi"].add_subplot(2,2,3))
        axes["deltaPhi"][2].set_ylabel("phi 3 [rad]")
        axes["deltaPhi"][2].set_xlabel("phi 4 [rad]")
        axes["deltaPhi"][2].scatter(self.phi['3'],self.phi['4'])
        axes["deltaPhi"].append(figures["deltaPhi"].add_subplot(2,2,4))
        axes["deltaPhi"][3].set_ylabel("entries")
        axes["deltaPhi"][3].set_xlabel("delta phi")
        axes["deltaPhi"][3].set_xlim(-0.2, 0.2)
        axes["deltaPhi"][3].hist(self.deltaPhi['34'], 200, normed=True)

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

        np.save("output/distributions.npy",
                    {
                    "X": self.X,
                    "phi":self.phi,
                    "Xc": self.Xc,
                    "phic":self.phic,
                    "deltaX":self.deltaX,
                    "deltaPhi":self.deltaPhi,
                    "trackPhi": self.trackPhi,
                    "trackX": self.trackX,
                    "eventTracksPhi": self.eventTracksPhi,
                    "eventTracksX": self.eventTracksX,
                    })
            
