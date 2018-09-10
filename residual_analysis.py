import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

import argparse
parser = argparse.ArgumentParser(description='analyze DT data')
parser.add_argument('-i', '--input', default="output/residuals.npy", help='The input file to analyze')
args = parser.parse_args()

data=np.load(args.input).item()
data=pd.DataFrame(data)
data=data[abs(data.residuals)<2]

x,y,erry=np.array([]),np.array([]),np.array([])
for i in np.arange(0,19.6,1.5):
    x=np.append(x,i+1.5/2)
    y=np.append(y,data[(data.distances>i) & (data.distances<=i+1.5)].residuals.mean())
    erry=np.append(erry,data[(data.distances>i) & (data.distances<=i+1.5)].residuals.std())    
    
slope, intercept, r_value, p_value, std_err = stats.linregress(data['distances'],data['residuals'])
print (std_err)
sns.jointplot(x=data['distances'], y=data['residuals'],kind="reg", color="k", marker="+",
                  line_kws={'label':"y={0:.3f}x+{1:.3f}".format(slope,intercept)}).set_axis_labels("distance from wire","residual")

plt.errorbar(x, y, yerr=erry, fmt='o',color="r")
plt.legend()


figure = plt.figure(num=2,figsize=(8,5))
plt.ylabel("entries")
plt.xlabel("hit-fit [mm]")
sns.distplot(data['residuals'], 80, kde=False, norm_hist=True)
mu, sigma = stats.norm.fit([x for x in data['residuals'] if -0.4<=x<=0.4])
#mu, sigma = stats.norm.fit(data['residuals'])
print (data['residuals'].mean(), data['residuals'].std())
print (mu, sigma)
x=np.linspace(-0.4, 0.4, 800)
pdf = stats.norm.pdf(x,loc=mu,scale=sigma)
plt.plot(x,pdf,'k-')

#sns.boxplot(x=data['distances'], y=data['residuals'])
plt.show()
