import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

import argparse
parser = argparse.ArgumentParser(description='analyze DT data')
parser.add_argument('-i', '--input', default="output/distributions.npy", help='The input file to analyze')
parser.add_argument("-l", "--leg", default="both", help="lines to be processed")
args = parser.parse_args()


# the input file
data=np.load(args.input).item()

# the leg of the experiment to be looked at
leg = args.leg

if leg=="pos" or leg =="neg":
    # 2D plots
    slope, intercept, r_value, p_value, std_err = stats.linregress(data['trackX'][leg],data['trackPhi'][leg])
    sns.jointplot(x=data['trackX'][leg], y=data['trackPhi'][leg],kind="reg", color="k", line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)})
    plt.legend()

    figure = plt.figure(num=2,figsize=(10,6))
    axes = []
    axes.append(figure.add_subplot(1,2,1))
    bins = np.linspace(-0.2, 0.2, 50)
    sns.distplot(data['trackPhi'][leg], bins, ax=axes[0], kde=False)
    axes.append(figure.add_subplot(1,2,2))
    #bins = np.linspace(data['trackX'][leg].min()-10)/100)*100,int((data['trackX'][leg].min()+10)/100)*100,50)
    sns.distplot(data['trackX'][leg], 50, ax=axes[1], kde=False) #norm_hist=True)



    
elif leg=="both":

    slope, intercept, r_value, p_value, std_err = stats.linregress(data['trackX']["pos"],data['trackPhi']["pos"])
    sns.jointplot(x=data['trackX']["pos"], y=data['trackPhi']["pos"],kind="reg", color="k", line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)})
    plt.legend()
    slope, intercept, r_value, p_value, std_err = stats.linregress(data['trackX']["neg"],data['trackPhi']["neg"])
    sns.jointplot(x=data['trackX']["neg"], y=data['trackPhi']["neg"],kind="reg", color="k", line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)})
    plt.legend()
#    slope, intercept, r_value, p_value, std_err = stats.linregress(data['trackX']["pos"],data['trackX']["neg"])
#    sns.jointplot(x=data['trackX']["pos"], y=data['trackX']["neg"],kind="reg", color="k", line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)})
#    plt.legend()
#    slope, intercept, r_value, p_value, std_err = stats.linregress(data['trackPhi']["pos"],data['trackPhi']["neg"])
#    sns.jointplot(x=data['trackPhi']["pos"], y=data['trackPhi']["neg"],kind="reg", color="k", line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)})
#    plt.legend()
#



plt.tight_layout()
plt.show()


