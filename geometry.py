import numpy as np
import matplotlib.pyplot as plt

z=np.array([-5.3328,-5.3319,-4.4313,-4.4322,-5.3341,-5.3343,-4.4341,-4.4315])
x=np.array([0.9565,0.2560,0.9629,0.2624,-0.2501,-0.9501,-0.2968,-0.9975])
l=["c4j","c4s","c3j","c3s","c2j","c2s","c1j","c1s"]

#plt.scatter(x,y)
#plt.show()

# chamber sizes:
out=[1e3*(x[l.index("c"+i+"s")]-x[l.index("c"+i+"j")]) for i in ["1","2","3","4"]]
print (out)

print ("x ditances between chambers at same z")
out = 1e3*(x[l.index("c4s")]-x[l.index("c2s")])
print ("saleve 4-2:", out)
out = 1e3*(x[l.index("c4j")]-x[l.index("c2j")])
print ("jura 4-2:", out)
out = 1e3*(x[l.index("c3s")]-x[l.index("c1s")])
print ("saleve 3-1:", out)
out = 1e3*(x[l.index("c3j")]-x[l.index("c1j")])
print ("jura 3-1:", out)

print ("x ditances between front and rear chambers")
out = 1e3*(x[l.index("c2s")]-x[l.index("c1s")])
print ("saleve 2-1:", out)
out = 1e3*(x[l.index("c2j")]-x[l.index("c1j")])
print ("jura 2-1:", out)
out = 1e3*(x[l.index("c4s")]-x[l.index("c3s")])
print ("saleve 4-3:", out)
out = 1e3*(x[l.index("c4j")]-x[l.index("c3j")])
print ("jura 4-3:", out)


print ("z ditances between chambers at same z")
out = 1e3*(z[l.index("c4s")]-z[l.index("c2s")])
print ("saleve 4-2:", out)
out = 1e3*(z[l.index("c4j")]-z[l.index("c2j")])
print ("jura 4-2:", out)
out = 1e3*(z[l.index("c3s")]-z[l.index("c1s")])
print ("saleve 3-1:", out)
out = 1e3*(z[l.index("c3j")]-z[l.index("c1j")])
print ("jura 3-1:", out)

print ("z ditances between front and rear chambers")
out = 1e3*(z[l.index("c2s")]-z[l.index("c1s")])
print ("saleve 2-1:", out)
out = 1e3*(z[l.index("c2j")]-z[l.index("c1j")])
print ("jura 2-1:", out)
out = 1e3*(z[l.index("c4s")]-z[l.index("c3s")])
print ("saleve 4-3:", out)
out = 1e3*(z[l.index("c4j")]-z[l.index("c3j")])
print ("jura 4-3:", out)

print("tilts")
tilts=[(z[l.index("c"+i+"s")]-z[l.index("c"+i+"j")])/(x[l.index("c"+i+"s")]-x[l.index("c"+i+"j")]) for i in ["1","2","3","4"]]
print ("tilts:", tilts)
out=tilts[1]-tilts[0]
print ("deltaphi 2-1:", out)
out=tilts[3]-tilts[2]
print ("deltaphi 4-3:", out)
