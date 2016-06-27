import random  # not for prod
import sys
from io import BytesIO

import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# os.chdir('./templates')  # not for prod
# print(os.getcwd())
# print(os.listdir())
from templates.tempData import coefficients

iter_ = 10000  # number of iterations for the Monte Carlo guesses. to be input on GUI

# INPUT
arrayType = 'wenner'
e = 5  # number of layers
n = 2 * e - 1

spac = 0.2  # smallest electrode spacing
m = 20  # number of points where resistivity is calculated

spac = np.log(spac)
delx = np.log(10.0) / 6.

# these lines apparently find the computer precision ep
ep = 1.0
ep = ep / 2.0
fctr = ep + 1.
while fctr > 1.:
    ep = ep / 2.0
    fctr = ep + 1.

schlumbergerFilterCoefficients, wennerFilterCoefficients = coefficients

# I know there must be a better method to assign lists. And probably numpy
# arrays would be best. But my Python wasn't up to it. If the last letter
# is an 'l' that means it is a log10 of the value

# 65 is completely arbitrary - > Nearing retirement?
p = [0] * 20
r = [0] * 65
rl = [0] * 65
t = [0] * 50
b = [0] * 65
asav = [0] * 65
asavl = [0] * 65
adatl = [0] * 65
rdatl = [0] * 65
adat = [0] * 65
rdat = [0] * 65
pkeep = [0] * 65
rkeep = [0] * 65
rkeepl = [0] * 65
pltanswer = [0] * 65
pltanswerl = [0] * 65
pltanswerkeep = [0] * 65
pltanswerkeepl = [0] * 65

rl = [0] * 65
small = [0] * 65
xlarge = [0] * 65

x = [0] * 100
y = [0] * 100
y2 = [0] * 100
u = [0] * 5000
new_x = [0] * 1000
new_y = [0] * 1000
ndat = 13
# hard coded data input - spacing and apparent resistivities measured
# in the field
adat = [0, 3., 4.5, 6., 9., 13.5, 21., 30., 45., 60., 90., 135., 210., 300.]
# adat = [0., 0.55, 0.95, 1.5, 2.5, 3., 4.5, 5.5, 9., 12., 20., 30.,  70.]
rdat = [0, 9295., 4475., 2068., 1494., 764., 375., 294., 245., 235., 156., 118., 83., 104.]
# rdat = [0., 125., 110., 95., 40., 24., 15., 10.5, 8., 6., 6.5, 11., 25.]
one30 = 1.e30
rms = one30
errmin = 1.e10
# this is where the range in parameters should be input from a GUI
# I'm hard coding this in for now

# enter thickness range for each layer and then resistivity range.
# for 3 layers small[1] and small[2] are low end [MINIMUM] of thickness range
# small[3], small[4] and small[5] are the low end [MINIMUM] of resistivities
small[1] = 1.
xlarge[1] = 30.

small[2] = 1.
xlarge[2] = 30.

small[3] = 1.
xlarge[3] = 30.

small[4] = 1.
xlarge[4] = 30.

small[5] = 1.
xlarge[5] = 1000000.

small[6] = 1.
xlarge[6] = 1000000.

small[7] = 1.
xlarge[7] = 1000000.

small[8] = 1.
xlarge[8] = 1000000.

small[9] = 1.
xlarge[9] = 1000000.


def montecarlo_sim(num_of_iterations, num_of_layers, errmin, ndat, adat, rdat):
    """

    Args:
        num_of_iter, num_of_layers,

    Return:

    """
    arrayType = 'wenner'  # used in rmsfit()
    # num_of_layers = 5  # number of layers
    n = 2 * num_of_layers - 1

    spac = 0.2  # smallest electrode spacing
    m = 20  # number of points where resistivity is calculated

    spac = np.log(spac)
    delx = np.log(10.0) / 6.

    # these lines apparently find the computer precision ep
    ep = 1.0
    ep = ep / 2.0
    fctr = ep + 1.
    while fctr > 1.:
        ep = ep / 2.0
        fctr = ep + 1.

    readData(ndat, adat, rdat)
    print('\naday, and rdat')
    print(adat[1:ndat], rdat[1:ndat])
    print('log stufffff')
    print(adatl[1:ndat], rdatl[1:ndat])
    print('small')
    print(small)
    print('xlarge')
    print(xlarge)

    for iloop in range(1, num_of_iterations + 1):
        # print( '  iloop is ', iloop)
        for i in range(1, n + 1):
            randNumber = random.random()
            # print(randNumber, '  random')
            p[i] = (xlarge[i] - small[i]) * randNumber + small[i]

        rms = rmsfit()

        if rms < errmin:
            print('rms  ', rms, '   errmin ', errmin)
            for i in range(1, n + 1, 1):
                pkeep[i] = p[i]
            for i in range(1, m + 1, 1):
                rkeep[i] = r[i]
                rkeepl[i] = rl[i]
            for i in range(1, ndat + 1, 1):
                pltanswerkeepl[i] = pltanswerl[i]
                pltanswerkeep[i] = pltanswer[i]
            errmin = rms

    # output the best fitting earth model
    print('\nLayer ', ' Thickness  ', '   Res_ohm-m  ')
    for i in range(1, e, 1):
        print('{:d}       {:9.6f}       {:9.6f}'.format(i, pkeep[i], pkeep[e + i - 1]))

    print(e, '      Infinite     ', pkeep[n])
    for i in range(1, m + 1, 1):
        asavl[i] = np.log10(asav[i])

    # output the error of fit
    print(' \n RMS error:', errmin, '\n')
    print('  Spacing', '  Res_pred  ', ' Log10_spacing  ', ' Log10_Res_pred ')
    for i in range(1, m + 1, 1):
        # print(asav[i], rkeep[i], asavl[i], rkeepl[i])
        print("%7.2f   %9.3f  %9.3f  %9.3f" % (asav[i], rkeep[i],
                                               asavl[i], rkeepl[i]))

    fig = plt.figure(figsize=(6, 3))
    plt.loglog(asav[1:m], rkeep[1:m], '-')  # resistivity prediction curve
    plt.loglog(adat[1:ndat], pltanswerkeep[1:ndat], 'ro')  # predicted data red dots
    plt.loglog(adat[1:ndat], rdat[1:ndat], 'bo', markersize=7)  # original datablue dots

    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data

    Image = ImageReader(imgdata)

    c = canvas.Canvas('figuretest.pdf', pagesize=letter)
    c.setLineWidth(.3)
    c.setFont('Courier', 10)

    c.drawString(50, 725, 'Date/Time:')
    c.drawString(50, 700, 'Drill: [ ]   No Drill: [ ]')

    c.drawString(260, 725, 'Lat/Long Coordinates:')
    c.drawString(260, 700, 'Bearing (Compass Direction Degrees):')
    c.drawString(50, 660, 'Root Mean Square Error: ')

    c.drawString(477, 310, 'Monte Carlo Sim')
    c.drawString(25, 300,
                 'Layer#  Min_Thickness  Max_Thickness  Min_Resistivity  Max_Resistivity  Thickness  Resistivity')

    c.drawImage(Image, 15, 350, height=275, preserveAspectRatio=True)
    c.save()
    # createPlot()
    # plt.show()
    # plt.grid(True)


def createPlot():
    plt.loglog(asav[1:m], rkeep[1:m], '-')  # resistivity prediction curve
    plt.loglog(adat[1:ndat], pltanswerkeep[1:ndat], 'ro')  # predicted data red dots
    plt.loglog(adat[1:ndat], rdat[1:ndat], 'bo', markersize=7)  # original datablue dots
    print('plt is type: {}'.format(type(plt)))
    createPDF()
    # plt.show()
    # plt.grid(True)


def createPDF():
    fig = plt.figure(figsize=(6, 3))

    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data

    Image = ImageReader(imgdata)

    c = canvas.Canvas('figuretest.pdf', pagesize=letter)
    c.setLineWidth(.3)
    c.setFont('Courier', 10)

    c.drawString(50, 725, 'Date/Time:')
    c.drawString(50, 700, 'Drill: [ ]   No Drill: [ ]')

    c.drawString(260, 725, 'Lat/Long Coordinates:')
    c.drawString(260, 700, 'Bearing (Compass Direction Degrees):')
    c.drawString(50, 660, 'Root Mean Square Error: ')

    c.drawString(477, 310, 'Monte Carlo Sim')
    c.drawString(25, 300,
                 'Layer#  Min_Thickness  Max_Thickness  Min_Resistivity  Max_Resistivity  Thickness  Resistivity')

    c.drawImage(Image, 15, 350, height=275, preserveAspectRatio=True)
    c.save()


def readData(ndat, adat, rdat):
    # normally this is where the data would be read from the csv file
    # but now I'm just hard coding it in as global lists

    for i in range(1, ndat, 1):
        adatl[i] = np.log10(adat[i])
        rdatl[i] = np.log10(rdat[i])

    return adatl


def error():
    sumerror = 0.
    # pltanswer = [0]*64
    spline(m, one30, one30, asavl, rl, y2)
    for i in range(1, ndat, 1):
        ans = splint(m, adatl[i], asavl, rl, y2)
        sumerror = sumerror + (rdatl[i] - ans) * (rdatl[i] - ans)
        # print(i,sum1,rdat[i],rdatl[i],ans)
        pltanswerl[i] = ans
        pltanswer[i] = np.power(10, ans)
    rms = np.sqrt(sumerror / (ndat - 1))

    return rms


def transf(y, i):
    u = 1. / np.exp(y)
    t[1] = p[n]
    for j in range(2, e + 1, 1):
        pwr = -2. * u * p[e + 1 - j]
        if pwr < np.log(2. * ep):
            pwr = np.log(2. * ep)
        a = np.exp(pwr)
        b = (1. - a) / (1. + a)
        rs = p[n + 1 - j]
        tpr = b * rs
        t[j] = (tpr + t[j - 1]) / (1. + tpr * t[j - 1] / (rs * rs))
    r[i] = t[e]
    return


def filters(b, k):
    for i in range(1, m + 1, 1):
        re = 0.
        for j in range(1, k + 1, 1):
            re = re + b[j] * r[i + k - j]
        r[i] = re
    return


def rmsfit():
    if arrayType.lower() == 'schlumberger':
        y = spac - 19. * delx - 0.13069
        mum1 = m + 28
        for i in range(1, mum1 + 1, 1):
            transf(y, i)
            y = y + delx
        filters(schlumbergerFilterCoefficients, 29)
    elif arrayType.lower() == 'wenner':
        s = np.log(2.)
        y = spac - 10.8792495 * delx
        mum2 = m + 33
        for i in range(1, mum2 + 1, 1):
            transf(y, i)
            a = r[i]
            y1 = y + s
            transf(y1, i)
            r[i] = 2. * a - r[i]
            y = y + delx
        filters(wennerFilterCoefficients, 34)
    else:
        print(" type of survey not indicated")
        sys.exit()

    x = spac
    for i in range(1, m + 1, 1):
        a = np.exp(x)
        asav[i] = a
        asavl[i] = np.log10(a)
        rl[i] = np.log10(r[i])
        x = x + delx

    rms = error()

    return rms


# my code to do a spline fit to predicted data at the nice spacing of Ghosh
# use splint to determine the spline interpolated prediction at the
# spacing where the measured resistivity was taken - to compare observation
# to prediction
def spline(n, yp1, ypn, x=[], y=[], y2=[]):
    u = [0] * 1000
    one29 = 0.99e30
    # print(x,y)
    if yp1 > one29:
        y2[0] = 0.
        u[0] = 0.
    else:
        y2[0] = -0.5
        u[0] = (3. / (x[1] - x[0])) * ((y[1] - y[0]) / (x[1] - x[0]) - yp1)

    for i in range(1, n):
        # print(i,x[i])
        sig = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
        p = sig * y2[i - 1] + 2.
        y2[i] = (sig - 1.) / p
        u[i] = (
            ((6. * ((y[i + 1] - y[i]) / (x[i + 1] - x[i]) - (y[i] - y[i - 1]) /
                    x[i] - x[i - 1])) / (x[i + 1] - x[i - 1]) - sig * u[i - 1]) / p)

    if ypn > one29:
        qn = 0.
        un = 0.
    else:
        qn = 0.5
        un = (
            (3. / (x[n] - x[n - 1])) *
            (ypn - (y[n] - y[n - 1]) /
             (x[n] - x[n - 1]))
        )

    y2[n] = (un - qn * u[n - 1]) / (qn * y2[n - 1] + 1.)
    for k in range(n - 1, -1, -1):
        y2[k] = y2[k] * y2[k + 1] + u[k]

    return


def splint(n, x, xa=[], ya=[], y2a=[]):
    klo = 0
    khi = n
    while khi - klo > 1:
        k = int((khi + klo) // 2)
        if xa[k] > x:
            khi = k
        else:
            klo = k
    h = xa[khi] - xa[klo]
    if abs(h) < 1e-20:
        print(" bad xa input")

    a = (xa[khi] - x) / h
    b = (x - xa[klo]) / h
    y = (a * ya[klo] + b * ya[khi] + ((a * a * a - a) * y2a[klo] +
                                      (b * b * b - b) * y2a[khi]) * (h * h) / 6.)

    return y


# main here
if __name__ == '__main__':

    montecarlo_sim(10000, 5, 1.e10)

    sys.exit(0)
