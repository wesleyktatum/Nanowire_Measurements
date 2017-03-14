import numpy as np
import math
import matplotlib.pyplot as plt

wire_image = np.loadtxt('100-0_72_NW-003')
#side = np.linspace(1,len(wire_image),len(wire_image))
side = np.linspace(1, 40, 40)
x, y = np.meshgrid(side, side)
plt.figure(1)
plt.contourf(x, y, wire_image[321:361, 321:361], cmap='bwr')
plt.colorbar()
plt.show()

single_wire = wire_image[321:361, 321:361]

for j in range(0, len(side)):
    for jj in range(0, len(side)):
        if single_wire[j, jj] < 0:
            single_wire[j, jj] = 0
        else:
            pass

count = np.zeros((len(side), len(side)))
top = np.max(single_wire)
bottom = np.min(single_wire)

for j in range(0, len(side)):
    for jj in range(0, len(side)):
        dist_from_top = top - single_wire[j, jj]
        dist_from_bottom = single_wire[j, jj] - bottom
        if dist_from_top < dist_from_bottom:
            count[j, jj] = 1
        else:
            count[j, jj] = 0

plt.figure(2)
plt.subplot(1, 2, 1)
plt.contourf(x, y, single_wire, cmap='bwr')
plt.colorbar()
plt.subplot(1, 2, 2)
plt.contourf(x, y, count, cmap='bwr', levels=[0, 0.5, 1])
plt.colorbar()
plt.tight_layout()
plt.show()
