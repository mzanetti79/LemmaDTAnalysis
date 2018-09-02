import numpy as np
import matplotlib.pyplot as plt

timens=np.load("output/timeboxes_331_selected.npy").item()
timensc=np.load("output/timeboxes_262.npy").item()

bins = np.linspace(-50, 500, 111)

plt.hist(timens[0].tolist()+timens[1].tolist()+timens[2].tolist()+timens[3].tolist(),bins, normed=True, label="331", alpha=0.5)
plt.hist(timensc[0].tolist()+timensc[1].tolist(),bins,normed=True, label="262", alpha=0.5)

plt.legend(loc='upper right')
plt.show()

