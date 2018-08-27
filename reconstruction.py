import numpy as np

import matplotlib.pyplot as plt


def fit(x, combinatorial):
    min_chi2=999999.
    for y in combinatorial:
        segment, residuals, _, _, _ = np.polyfit(x, y, 1, full=True)
        chi2 = residuals/(len(x)-2)
        if  chi2 < min_chi2:
            min_chi2 = chi2
            best_segment = np.poly1d(segment) 
    return best_segment
    

def reconstruct(selectedhits, verbose=False):
    result = {}
    for chamber in selectedhits.chamber.unique():

        # get the hits in the chamber
        chamberhits = selectedhits[(selectedhits.chamber==chamber)]

        # get the hits in the 4 layers. Empty array in case there are none in a given layer
        layerhits = np.array([chamberhits[chamberhits.layer==1].globalxleft.tolist() + chamberhits[chamberhits.layer==1].globalxright.tolist(),
                              chamberhits[chamberhits.layer==2].globalxleft.tolist() + chamberhits[chamberhits.layer==2].globalxright.tolist(),
                              chamberhits[chamberhits.layer==3].globalxleft.tolist() + chamberhits[chamberhits.layer==3].globalxright.tolist(),
                              chamberhits[chamberhits.layer==4].globalxleft.tolist() + chamberhits[chamberhits.layer==4].globalxright.tolist()
                              ])


        # the case with hits in 4 layers
        if len(chamberhits.globalz.unique())==4:
            x = np.array([chamberhits[chamberhits.layer==1].globalz.unique()[0],
                          chamberhits[chamberhits.layer==2].globalz.unique()[0],
                          chamberhits[chamberhits.layer==3].globalz.unique()[0],
                          chamberhits[chamberhits.layer==4].globalz.unique()[0]])
            combinatorial = np.array(np.meshgrid(layerhits[0], layerhits[1], layerhits[2], layerhits[3])).T.reshape(-1,4)


        # alternatively get the hits in at least3 layers.
        elif len(chamberhits.globalz.unique())==3:
            layers_with_hits = [i for i,j in enumerate(layerhits) if len(j)!=0]
            x = np.array([chamberhits[chamberhits.layer==layers_with_hits[0]+1].globalz.unique()[0],
                          chamberhits[chamberhits.layer==layers_with_hits[1]+1].globalz.unique()[0],
                          chamberhits[chamberhits.layer==layers_with_hits[2]+1].globalz.unique()[0]])
            combinatorial = np.array(np.meshgrid(layerhits[layers_with_hits[0]], layerhits[layers_with_hits[1]], layerhits[layers_with_hits[2]])).T.reshape(-1,3)

        # not performing fit with less layers
        else: continue
            
        if verbose:
            print ("reconstructing chamber",chamber)
            print ("resolving the following",len(combinatorial),"combinations")
            print (combinatorial)
            
        result[chamber] = fit(x, combinatorial)
        if verbose:
            print ("best fit:", result[chamber])
            
    return result
                    
