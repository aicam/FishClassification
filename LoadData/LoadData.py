import os
from scipy.io import loadmat
import numpy as np
import pandas as pd
from ... import configFile


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

def getTrainTestDict():
    '''
    :return: generates folds based on K value specified in config file out of dataframes
    '''
    VNIR_DF, Fluor_DF, SWIR_DF = getData()
    trainTestDict = {}
    for f in range(cfg.nFolds):
        fold = f + 1
        foldName = 'Fold' + str(fold)
        trainTestDict[foldName] = {}
        trainTestDict[foldName]['VNIR_trainDF'], trainTestDict[foldName]['VNIR_testDF'] = getTrainTest(VNIR_DF, fold)
        trainTestDict[foldName]['Fluor_trainDF'], trainTestDict[foldName]['Fluor_testDF'] = getTrainTest(Fluor_DF, fold)
        trainTestDict[foldName]['SWIR_trainDF'], trainTestDict[foldName]['SWIR_testDF'] = getTrainTest(SWIR_DF, fold)
        return trainTestDict