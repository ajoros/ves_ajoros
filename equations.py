import numpy as np


def wenner(a, Vm, I):
    return (2 * np.pi * a * (Vm / I))


def schlumberger(Vm, L, s, I):
    return ((np.pi * Vm (L**2 - s**2)) / (2 * s * I))
