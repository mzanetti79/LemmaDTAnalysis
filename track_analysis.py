import matplotlib
matplotlib.use('TkAgg')
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

BL=1.7476*2
rigidity=0.3*BL
m_mu=0.10166


def sqrts(phi1,phi2):
    phi1,phi2=abs(phi1),abs(phi2) # just to be sure signs are correct..
    try: s = 2*m_mu**2+pow(phi1+phi2,2)*rigidity**2/phi1/phi2
    except: s = 0 
    return np.sqrt(s)

# the input file
data=np.load(args.input).item()

# the leg of the experiment to be looked at
leg = args.leg

if leg=="pos" or leg =="neg":
    # 2D plots
    slope, intercept, r_value, p_value, std_err = stats.linregress(data['trackX'][leg],data['trackPhi'][leg])
    sns.jointplot(x=data['trackX'][leg], y=data['trackPhi'][leg],kind="reg", color="k",
                      line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)}).set_axis_labels("X [mm]", "angle [rad]")
    plt.legend()

    figure = plt.figure(num=2,figsize=(10,6))
    axes = []
    axes.append(figure.add_subplot(1,2,1))
    axes[0].set_ylabel("entries")
    axes[0].set_xlabel("momentum [GeV/c]")
    #bins = np.linspace(-0.2, 0.2, 50)
    bins = np.linspace(10, 30, 40)
    sns.distplot(abs(rigidity/data['trackPhi'][leg]), bins, ax=axes[0], kde=False, norm_hist=True)

    mu, sigma = stats.norm.fit([x for x in abs(rigidity/data['trackPhi'][leg]) if 11<=x<=20])
    print (mu, sigma)
    x=np.linspace(11, 20, 800)
    pdf = stats.norm.pdf(x,loc=mu,scale=sigma)
    #plt.plot(x,pdf,'k-')

    
    axes.append(figure.add_subplot(1,2,2))
    axes[1].set_ylabel("entries")
    axes[1].set_xlabel("X [mm]")
    #bins = np.linspace(data['trackX'][leg].min()-10)/100)*100,int((data['trackX'][leg].min()+10)/100)*100,50)
    sns.distplot(data['trackX'][leg], 50, ax=axes[1], kde=False) #norm_hist=True)



    
elif leg=="both":

    slope, intercept, r_value, p_value, std_err = stats.linregress(data['trackX']["pos"],data['trackPhi']["pos"])
    sns.jointplot(x=data['trackX']["pos"], y=data['trackPhi']["pos"],kind="reg", color="k",
                      line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)}).set_axis_labels("X [mm]", "angle [rad]")
    plt.legend()
    slope, intercept, r_value, p_value, std_err = stats.linregress(data['trackX']["neg"],data['trackPhi']["neg"])
    sns.jointplot(x=data['trackX']["neg"], y=data['trackPhi']["neg"],kind="reg", color="k",
                      line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)}).set_axis_labels("X [mm]", "angle [rad]")
    plt.legend()

    slope, intercept, r_value, p_value, std_err = stats.linregress(data['eventTracksX']["pos"],data['eventTracksX']["neg"])
    sns.jointplot(x=data['eventTracksX']["pos"], y=data['eventTracksX']["neg"],kind="reg", color="k",
                      line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)}).set_axis_labels("X + [mm]", "X - [mm]")
    plt.legend()
    slope, intercept, r_value, p_value, std_err = stats.linregress(data['eventTracksPhi']["pos"],data['eventTracksPhi']["neg"])
    sns.jointplot(x=data['eventTracksPhi']["pos"], y=data['eventTracksPhi']["neg"],kind="reg", color="k",
                      line_kws={'label':"y={0:.5f}x+{1:.3f}".format(slope,intercept)}).set_axis_labels("angle + [rad]", "angle - [rad]")

    figure = plt.figure(num=10,figsize=(10,6))
    axes = []
    axes.append(figure.add_subplot(1,2,1))
    #bins = np.linspace(0, 0.2, 50)
    #sns.distplot(data['eventTracksPhi']['pos'], bins, ax=axes[0], kde=False, label="positive leg")
    #sns.distplot(-data['eventTracksPhi']['neg'], bins, ax=axes[0], kde=False, label="negative leg")
    axes[0].set_ylabel("entries")
    axes[0].set_xlabel("momentum [GeV/c]")
    axes[0].set_xlim(10, 40)
    bins=np.arange(10, 40 + 1, 1)
    sns.distplot(abs(rigidity/data['eventTracksPhi']['pos']), bins, ax=axes[0], kde=False, label="positive leg")
    sns.distplot(abs(rigidity/data['eventTracksPhi']['neg']), bins, ax=axes[0], kde=False, label="negative leg")
    plt.legend()
    
    axes.append(figure.add_subplot(1,2,2))
    axes[1].set_ylabel("entries")
    axes[1].set_xlabel("X [mm]")
    sns.distplot(data['eventTracksX']['pos'], 40, ax=axes[1], kde=False)
    sns.distplot(-data['eventTracksX']['neg'], 40, ax=axes[1], kde=False)
    


plt.tight_layout()
plt.show()


