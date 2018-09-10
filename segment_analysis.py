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
parser.add_argument("-l", "--leg", default="neg", help="lines to be processed")
args = parser.parse_args()

data=np.load(args.input).item()

if args.leg=="neg": ch1,ch2="1","2"
else: ch1,ch2="3","4"


# it creates its own figure
slope, intercept, r_value, p_value, std_err = stats.linregress(data['phic'][ch1],data['phic'][ch2])
sns.jointplot(x=data['phic'][ch1], y=data['phic'][ch2],kind="reg", color="k",
                  line_kws={'label':"y={0:.3f}x+{1:.3f}".format(slope,intercept)}).set_axis_labels("angle ch"+str(ch1), "angle ch"+str(ch2))
plt.legend()
slope, intercept, r_value, p_value, std_err = stats.linregress(data['Xc'][ch1],data['Xc'][ch2])
sns.jointplot(x=data['Xc'][ch1], y=data['Xc'][ch2],kind="reg", color="k",
                  line_kws={'label':"y={0:.3f}x+{1:.3f}".format(slope,intercept)}).set_axis_labels("X ch"+str(ch1), "X ch"+str(ch2))
plt.legend()

# now draw the 1D distributions
# phi
figure = plt.figure(num=3,figsize=(10,6))
axes = []
axes.append(figure.add_subplot(1,2,1))
axes[0].set_ylabel("entries")
axes[0].set_xlabel("bending angle [rad]")
axes[0].set_xlim(-0.2, 0.2)
sns.distplot(data['phi'][ch1], 50, label='chamber '+ch1, ax=axes[0], kde=False)
sns.distplot(data['phi'][ch2], 50, label='chamber '+ch2, ax=axes[0], kde=False)
plt.legend(loc='upper right')
axes.append(figure.add_subplot(1,2,2))
axes[1].set_ylabel("entries")
axes[1].set_xlabel("bending angle difference [rad]")
axes[1].set_xlim(-0.2, 0.2)
sns.distplot(data['deltaPhi'][ch1+ch2], 50, ax=axes[1], kde=False, norm_hist=True)

# X
figure = plt.figure(num=4,figsize=(10,6))
axes.append(figure.add_subplot(1,2,1))
axes[2].set_ylabel("entries")
axes[2].set_xlabel("X [mm]")
#axes[2].set_xlim(-900, -200)
sns.distplot(data['X'][ch1], 50, label='chamber '+ch1, ax=axes[2], kde=False, norm_hist=True)
sns.distplot(data['X'][ch2], 50, label='chamber '+ch2, ax=axes[2], kde=False, norm_hist=True)
plt.legend(loc='upper right')
axes.append(figure.add_subplot(1,2,2))
axes[3].set_ylabel("entries")
axes[3].set_xlabel("X difference [mm]")
#axes[3].set_xlim(-900, -200)
sns.distplot(data['deltaX'][ch1+ch2+"at"+ch1], 50, ax=axes[3], kde=False, norm_hist=True)


if False:
    # fit in the bulk
    ranges={"1":[0.02,0.1],"2":[0.02,0.1],"3":[-0.1,-0.02],"4":[-0.1,-0.02]}
    mu,sigma, pdf = {},{},{}
    (mu[1], sigma[1]) = stats.norm.fit([x for x in data['phi'][ch1] if ranges[ch1][0]<=x<=ranges[ch1][1]])
    (mu[2], sigma[2]) = stats.norm.fit([x for x in data['phi'][ch2] if ranges[ch1][0]<=x<=ranges[ch1][1]])
    print (mu, sigma)
    x=np.linspace(-0.2, 0.2, 800)
    for i in [1,2]: pdf[i] = stats.norm.pdf(x,loc=mu[i],scale=sigma[i])
    plt.plot(x,pdf[1],'k-',x,pdf[2],'k-')

#plt.tight_layout()
plt.show()

