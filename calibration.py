import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from configuration import *


class calibrator():
    def __init__(self):
        self.timens = {0:np.array([]),1:np.array([]),2:np.array([]),3:np.array([])}

    def update(self, selectedhits):
        chambers = selectedhits.chamber.unique()
        for chamber in chambers: self.timens[chamber]=np.append(self.timens[chamber],selectedhits[selectedhits.chamber==chamber].timens)


    def fit(self):
        return 0
    
    def plot(self):
        figure = plt.figure(figsize=(10,8))
        axes=[]
        for i in range(0,4):
            axes.append(figure.add_subplot(2,2,i+1))
            axes[i].set_ylabel("entries")
            axes[i].set_xlabel("corrected time [ns]")
            axes[i].set_xlim(-100, 700)
            axes[i].set_title("Chamber"+str(i+1))
            axes[i].hist(self.timens[i],400)
        plt.tight_layout()
        plt.show()

    def save(self):
        np.save("output/timeboxes.npy", self.timens)
        
