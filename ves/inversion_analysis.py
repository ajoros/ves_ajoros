import sys

import numpy as np
from PyQt5.QtWidgets import QApplication

from aggregate import aggregateTable
import equations
from main import StartupWindow
from templates.tempData import colors, headers, tableData, old_coefficients


def inversionAnalysis(apparentResistivity, voltageSpacing,
                       rectangleCoordinates, arraySpacing,
                       iterations=10000,
                       smallestSpacing=(np.log(0.2)),
                       p=[0., 2., 30., 100., 10., 2000.],
                       sampleInterval=(np.log(10) / 6.),
                       ep=0.5):
    nLayers = len(rectangleCoordinates)
    # these lines apparently find the computer precision ep
    fctr = ep + 1.

    while fctr > 1.:
        ep = ep / 2.
        fctr = ep + 1.

    layerThickness, layerResistivity = thicknessResistivityCalculation(
        rectangleCoordinates)

    print(layerThickness)
    print(layerResistivity)

def thicknessResistivityCalculation(rectangleCoordinates):

    (minLayerThickness, maxLayerThickness,
     minLayerRestivity, maxLayerResitivity) = (np.array([]), np.array([]),
                                               np.array([]), np.array([]))
    for rectangle in rectangleCoordinates:
        # xy will be the origin of drawing, and height and width are positive
        #  or negative appropriately. Hence, adding height/width should always
        #  satisfy the problem of determining distance from the origin in
        #  a positive coordinate space. No abs() needed.
        xy, width, height = rectangle

        thicknessValues = np.array([xy[0], xy[0] + width])
        resistivityValues = np.array([xy[1], xy[1] + height])

        minLayerThickness = np.append(
            minLayerThickness, np.min(thicknessValues))
        maxLayerThickness = np.append(
            maxLayerThickness, np.max(thicknessValues))

        minLayerRestivity = np.append(
            minLayerRestivity, np.min(resistivityValues))
        maxLayerResitivity = np.append(
            maxLayerResitivity, np.max(resistivityValues))

    # Return NumPy array objects with min values index:0, max index:1
    # layerThickness = np.array([minLayerThickness, maxLayerThickness])
    # layerResistivity = np.array([minLayerRestivity, maxLayerResitivity])

    # Return dictionary of numpy arrays with keys set as min or max strings
    layerThickness = {'min': minLayerThickness, 'max': maxLayerThickness}
    layerResistivity = {'min': minLayerRestivity, 'max': maxLayerResitivity}

    return layerThickness, layerResistivity


def transform(y, nLayers):
    n = 2 * nLayers - 1
    u = 1. / np.exp(y)




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
        0., 0.55, 0.95, 1.5, 2.5, 3., 4.5, 5.5, 9., 12., 20., 30.,  70.]
    apparentResistivity = [
        0., 125., 110., 95., 40., 24., 15., 10.5, 8., 6., 6.5, 11., 25.]

    inversionAnalysis(
        voltageSpacing, apparentResistivity, main.canvas.rectCoordinates,
        'schlumberger')

    # print(np.log(voltageSpacing))
    # print(np.log(apparentResistivity))