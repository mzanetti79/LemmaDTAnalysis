import numpy as np

class residuals_estimator():
    def __init__(self):
        self.distances, self.residuals = np.array([]), np.array([])    

        
    def compute(self, selectedhits, segmenthits, segments):
        for chamber in segmenthits:
            for i, x in enumerate(segmenthits[chamber]["x"]): 
                fithit = segments[chamber](x)
                wires = selectedhits[(selectedhits.chamber==chamber) & (selectedhits.globalz==x)].globalxmean.tolist() 
                wire = wires[[abs(j-fithit) for j in wires].index(min([abs(j-fithit) for j in wires]))]
                hits = selectedhits[selectedhits.globalz==x].globalxleft.tolist() # just one is needed
                distance = min([abs(j-wire) for j in hits])
                self.distances=np.append(self.distances,distance)
                self.residuals=np.append(self.residuals, distance-abs(wire-fithit))


    def save(self):
        np.save("output/residuals.npy",
                    {
                    "distances": self.distances,
                    "residuals": self.residuals
                    })
