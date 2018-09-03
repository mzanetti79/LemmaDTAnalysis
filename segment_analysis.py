import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


data=np.load("output/distributions.npy").item()


ch1,ch2="1","2"

ch1,ch2="3","4"

ranges={"1":[0.02,0.1],"2":[0.02,0.1],"3":[-0.1,-0.02],"4":[-0.1,-0.02]}

# it creates its own figure
slope, intercept, r_value, p_value, std_err = stats.linregress(data['phi'][ch1],data['phi'][ch2])
sns.jointplot(x=data['phi'][ch1], y=data['phi'][ch2],kind="reg", color="k", line_kws={'label':"y={0:.3f}x+{1:.3f}".format(slope,intercept)})
plt.legend()

# now draw the 1D distributions
figure = plt.figure(num=2,figsize=(10,6))
axes = []
axes.append(figure.add_subplot(1,2,1))
bins = np.linspace(-0.2, 0.2, 50)
sns.distplot(data['phi'][ch1], bins, label='chamber '+ch1, ax=axes[0], kde=False, norm_hist=True)
sns.distplot(data['phi'][ch2], bins, label='chamber '+ch2, ax=axes[0], kde=False, norm_hist=True)
plt.legend(loc='upper right')
# fit in the bulk
mu,sigma, pdf = {},{},{}
(mu[1], sigma[1]) = stats.norm.fit([x for x in data['phi'][ch1] if ranges[ch1][0]<=x<=ranges[ch1][1]])
(mu[2], sigma[2]) = stats.norm.fit([x for x in data['phi'][ch2] if ranges[ch1][0]<=x<=ranges[ch1][1]])
print (mu, sigma)
x=np.linspace(-0.2, 0.2, 800)
for i in [1,2]: pdf[i] = stats.norm.pdf(x,loc=mu[i],scale=sigma[i])
plt.plot(x,pdf[1],'k-',x,pdf[2],'k-')

axes.append(figure.add_subplot(1,2,2))
#sns.distplot(data['deltaPhi']['12'], bins, ax=axes[1], kde=False, norm_hist=True)
sns.distplot(data['deltaPhi']['34'], bins, ax=axes[1], kde=False, norm_hist=True)
#axes.append(figure.add_subplot(2,1,2))
plt.tight_layout()
plt.show()

