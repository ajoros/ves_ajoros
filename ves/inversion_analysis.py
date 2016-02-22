import sys

import numpy as np
from PyQt5.QtWidgets import QApplication

from aggregate import aggregateTable
import equations
from main import StartupWindow
from templates.tempData import (
    colors, headers, tableData, coefficients, old_coefficients)


def inversionAnalysis(apparentResistivity, voltageSpacing,
                      rectangleCoordinates, arraySpacing,
                      iterations=10000,
                      smallestSpacing=0.2,
                      p=[0., 2., 30., 100., 10., 2000.],
                      sampleInterval=(np.log(10) / 6.),
                      ep=1.0, nOuputPoints=20, errMin=1.e10):

    nLayers = len(rectangleCoordinates)
    n = 2 * nLayers - 1                       # number of layer depths
    smallestSpacing = np.log(smallestSpacing)
    # m = number of points where resistivity will be calculated = nOutputPoints

    layerThickness, layerResistivity = thicknessResistivityFromRectangles(
        rectangleCoordinates)


    logVoltageSpacing = np.log(voltageSpacing)
    logApparentResistivity = np.log(apparentResistivity)

    if arraySpacing == 'schlumberger':
        pass
    elif arraySpacing == 'wenner':
        pass
    else:
        print('Improper array spacing selected. ' +
              'Must be schlumberger or wenner')
        sys.exit()

    thickParam, resParam = calcEarthParams(layerThickness, layerResistivity)
    print('\nthickParam\n{}'.format(thickParam))
    print('resParam\n{}'.format(resParam))

    # these lines apparently find the computer precision ep
    fctr = ep + 1.
    ep = ep / 2.
    while fctr > 1.:
        ep = ep / 2.
        fctr = ep + 1.

    for mcIter in range(iterations):
        rmsError = rmsFit(
            thickParam, resParam, apparentResistivity,
            smallestSpacing, sampleInterval,
            nOuputPoints, arraySpacing)
        print(rmsError)


def transform(y, ep):
    """"""
    u = 1. / np.exp(y)
    pwrThickness = -2. * u * thicknessParameters
    pwrResistivity = -2. * u * resistivityParameters

    return y + sampleInterval




def rmsFit(thicknessParameters, resistivityParameters, apparentResistivity,
           smallestSpacing, sampleInterval, nOuputPoints, arraySpacing):
    """"""
    if arraySpacing == 'schlumberger':
        y = spac - 10.8792495 * sampleInterval
        nFilterCoefficients = m + 33

        y = smallestSpacing - 10.8792495 * sampleInterval + np.log(2.)
        y = trasform(y)

        # for i in range(m + 33):


def calcEarthParams(layerThickness, layerResistivity):
    """"""
    nLayers = len(layerResistivity['min']) # or 'max'
    thicknessParam = np.empty((nLayers, ))
    resistivityParam = np.empty((nLayers, ))

    # Iterate through the layers, applying the p formula to both
    #  thickness and resistivity
    for i in range(nLayers):
        # Generate a random number to control where in the range of
        #  possible values the true value of p could lie. This precedes the
        #  MC iteration, so take one p value with a grain of salt, but many
        #  with a salt shaker
        randomNumber = np.random.random_sample()
        if i < (nLayers - 1): # Skip last depth (infinite)
            thicknessP = (
                (layerThickness['max'][i] - layerThickness['min'][i]) *
                 randomNumber + layerThickness['min'][i])

            thicknessParam = np.insert(thicknessParam, i, thicknessP)
            del thicknessP

        resistivityP = (
            (layerResistivity['max'][i] - layerResistivity['min'][i]) *
             randomNumber + layerResistivity['min'][i])

        resistivityParam = np.insert(resistivityParam, i, resistivityP)
        del resistivityP

    return (thicknessParam[:nLayers - 1], resistivityParam[:nLayers])


def thicknessResistivityFromRectangles(rectangleCoordinates):

    (minLayerThickness, maxLayerThickness,
     minLayerResistivity, maxLayerResitivity) = (np.array([]), np.array([]),
                                                 np.array([]), np.array([]))
    for rectangle in rectangleCoordinates:
        # xy will be the origin of drawing, and height and width are positive
        #  or negative appropriately. Hence, adding height/width should always
        #  satisfy the problem of determining distance from the origin in
        #  a positive coordinate space. No abs() needed.
        xy, width, height = rectangle

        thicknessValue = np.array([xy[0], xy[0] + width])    # x-axis
        resistivityValue = np.array([xy[1], xy[1] + height]) # y-axis

        minLayerThickness = np.append(
            minLayerThickness, np.min(thicknessValue))
        maxLayerThickness = np.append(
            maxLayerThickness, np.max(thicknessValue))

        minLayerResistivity = np.append(
            minLayerResistivity, np.min(resistivityValue))
        maxLayerResitivity = np.append(
            maxLayerResitivity, np.max(resistivityValue))


    # Return NumPy array objects with min values index:0, max index:1
    # layerThickness = np.array([minLayerThickness, maxLayerThickness])
    # layerResistivity = np.array([minLayerResistivity, maxLayerResitivity])

    # Return dictionary of numpy arrays with keys set as min or max strings
    layerThickness = {'min': minLayerThickness, 'max': maxLayerThickness}
    layerResistivity = {'min': minLayerResistivity, 'max': maxLayerResitivity}

    # Last layer goes to infinity
    layerThickness['max'][-1] = np.inf

    minThicknessResistivity = np.array(
        [minLayerResistivity[:-1], minLayerThickness])
    # maxThicknessResisttivi
    return layerThickness, layerResistivity


def transform(y, nLayers):
    n = 2 * nLayers - 1
    u = 1. / np.exp(y)


def rmse(observedValues, predictedValues):

    error = np.sqrt((predictedValues - observedValues) ** 2).mean()

    return error




if __name__ == '__main__':

    app = QApplication(sys.argv)

    # Spin up a main instance similar to what will exist after GUI input
    main = StartupWindow(tableData, headers, colors, old_coefficients)
    main.schlumberger()
    main.compute()
    rectangleCoordinates = [
    ((0.46988146917194829, 1267.1859604732258),
      3.9293328705180155, -916.78591585951676),

    ((4.3992143396899639, 350.4000446137091),
      19.549059554293287, 475.15927793601833),

    ((25.627732384051342, 807.14947142848234),
      36.227680367632061, 579.6626526304766)]
    for rectangle in rectangleCoordinates:
        main.canvas.rectxy = rectangle
        main.newRectangle()

    # s = input('s')

    voltageSpacing = [
        0.55, 0.95, 1.5, 2.5, 3., 4.5, 5.5, 9., 12., 20., 30.,  70.]
    apparentResistivity = [
        125., 110., 95., 40., 24., 15., 10.5, 8., 6., 6.5, 11., 25.]

    inversionAnalysis(
        voltageSpacing, apparentResistivity, main.canvas.rectCoordinates,
        'schlumberger')

    # print(np.log(voltageSpacing))
    # print(np.log(apparentResistivity))

    #