import numpy as np

import matplotlib.pyplot as plt


def fit(x, combinatorial):
    min_chi2=999999.
    for y in combinatorial:
        segment, residuals, _, _, _ = np.polyfit(x, y, 1, full=True)
        # only segments with a reasonable slope are considered 
        #if abs(np.poly1d(segment).c[0])>0.2: continue
        chi2 = residuals/(len(x)-2)
        if  chi2 < min_chi2:
            min_chi2 = chi2
            best_segment = np.poly1d(segment)
            best_combination = y
    return best_segment, {"x": x, "y":best_combination}
    

def segment_reconstructor(selectedhits, verbose=False):
    segments, best_hits = {}, {}
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

        # resolve combinatorial and reconstruct the best segments
        segments[chamber], best_hits[chamber] = fit(x, combinatorial)
        if verbose: print ("best fit:", segments[chamber], best_hits)
            
    return segments, best_hits
                    
def track_reconstructor(hits, verbose=False):

    tracks = {}

    # negative side
    if all(x in hits.keys() for x in [2, 3]):
        negative_leg_hits_x = np.append(hits[2]["x"],hits[3]["x"])
        negative_leg_hits_y = np.append(hits[2]["y"],hits[3]["y"])
        track, residuals, _, _, _ = np.polyfit(negative_leg_hits_x, negative_leg_hits_y, 1, full=True)
        tracks["neg"] = np.poly1d(track)
        if verbose: print (tracks["neg"])


    # positive side
    if all(x in hits.keys() for x in [0, 1]):
        positive_leg_hits_x = np.append(hits[0]["x"],hits[1]["x"])
        positive_leg_hits_y = np.append(hits[0]["y"],hits[1]["y"])
        track, residuals, _, _, _ = np.polyfit(positive_leg_hits_x, positive_leg_hits_y, 1, full=True)
        tracks["pos"] = np.poly1d(track)
        if verbose: print (tracks["pos"])

        
    return tracks
