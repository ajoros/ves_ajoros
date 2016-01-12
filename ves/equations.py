import numpy as np


def wennerResistivity(a, Vm, I):

    return 2 * np.pi * a * (Vm / I)


def schlumbergerResistivity(Vm, L, s, I):

    return (np.pi * Vm * (L**2 - s**2)) / (2 * s * I)


def schlumbergerResistivityModified(ab, Vm, I):

    return np.pi * Vm * ab / 2 * (Vm / I)