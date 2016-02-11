# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 16:32:48 2016

@author: jclark

this code uses teh Ghosh method to determine the apparent resistivities
for a layered earth model. Either schlumberger or Wenner configurations
can be used
"""
import sys

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

# Schlumberger filter
fltr1 = [0., .00046256, -.0010907, .0017122, -.0020687,
         .0043048, -.0021236, .015995, .017065, .098105, .21918, .64722,
         1.1415, .47819, -3.515, 2.7743, -1.201, .4544, -.19427, .097364,
         -.054099, .031729, -.019109, .011656, -.0071544, .0044042,
         -.002715, .0016749, -.0010335, .00040124]

#Wenner Filter
fltr2 = [0., .000238935, .00011557, .00017034, .00024935,
         .00036665, .00053753, .0007896, .0011584, .0017008, .0024959,
         .003664, .0053773, .007893, .011583, .016998, .024934, .036558,
         .053507, .078121, .11319, .16192, .22363, .28821, .30276, .15523,
         -.32026, -.53557, .51787, -.196, .054394, -.015747, .0053941,
         -.0021446, .000665125]

r = [0] * 65
t = [0] * 50
b = [0] * 65
asav = [0] * 65
asavl = [0] * 65
rl = [0] * 65

# INPUT
index = 1   # 1 is for shchlumberger and 2 is for Wenner
n_layers = 3   #number of layers
n = 2 * n_layers - 1

# e-1 thicknesses first and then e resistivity values
p = [0., 2., 30., 100., 10., 2000.]

spac = np.log(0.5) # smallest electrode spacing
m = 20

delx = np.log(10.0) / 6.

# these lines apparently find the computer precision ep
ep = 1.
ep = ep / 2.
fctr = ep + 1.

while fctr > 1.:
    ep = ep / 2.
    fctr = ep + 1.
    # print('{} {}'.format(fctr, ep))

def transf(y, i):
    u = 1. / np.exp(y)
    t[1] = p[n]
    for j in range(2, n_layers + 1):
        pwr = -2. * u * p[n_layers + 1 - j]
        if pwr < np.log(2. * ep):
            pwr = np.log(2. * ep)
        a = np.exp(pwr)
        b = (1. - a) / (1. + a)
        rs = p[n + 1 - j]
        tpr = b * rs
        t[j] = (tpr + t[j - 1]) / (1. + tpr * t[j-1] / (rs * rs))
    r[i] = t[n_layers]
    return


def filters(b, k):
    for i in range(1, m + 1):
        re = 0.
        for j in range(1, k + 1, 1):
            re = re + b[j] * r[i + k - j]
        r[i] = re
    return


if index == 1:
    y = spac - 19. * delx - 0.13069
    mum1 = m + 28
    print(y)
    for i in range(1, mum1 + 1, 1):
        transf(y, i)
        y = y + delx
    print(y)
    filters(fltr1, 29)
elif index == 2:
    s = np.log(2.)
    y = spac -10.8792495 * delx
    mum2 = m + 33
    for i in range(1, mum2+1, 1):
        transf(y, i)
        a = r[i]
        y1 = y + s
        transf(y1, i)
        r[i] = 2. * a - r[i]
        y = y + delx
    filters(fltr2, 34)
else:
    print(" type of survey not indicated")
    sys.exit()

x = spac
print("A-Spacing   App. Resistivity")
for i in range(1, m+1, 1):
    a = np.exp(x)
    asav[i] = a
    asavl[i] = np.log10(a)
    rl[i] = np.log10(r[i])
    x = x + delx
    print("%7.2f   %9.3f " % ( asav[i], r[i]))
print(asav)
print(r)

plt.loglog(asav[:20], r[:20])
plt.show()
