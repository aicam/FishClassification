import os
from scipy.io import loadmat
import numpy as np
import pandas as pd
import configFile as cfg


def getWavelengths(mode):
    '''
    :param mode: mode of fillet scanning
    :return: dataset (loadmat) of specified scanning method
    '''

    # Load data
    wavelengths = loadmat(cfg.wavelengthsPath)

    if mode == 'VNIR':
        return wavelengths['wavelength_vs'].flatten()
    elif mode == 'Fluor':
        return wavelengths['wavelength_fl'].flatten()
    elif mode == 'SWIR':
        return wavelengths['wavelength_ir'].flatten()[16:132]
    else:
        return None

if __name__ == '__main__':
    wavelengths = getWavelengths('SWIR')
