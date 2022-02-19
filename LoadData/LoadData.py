import os
from scipy.io import loadmat
import numpy as np
import pandas as pd
import configFile as cfg

'''
    The class contains all required methods, variable and configurations required to load our train and test dataset
'''
class DataGenerator:
    def __init__(self, mode):
        self.mode = mode

    def getWavelengths(self):
        '''
        :param mode: mode of fillet scanning
        :return: dataset (loadmat) of specified scanning method
        '''
        # Load data
        wavelengths = loadmat(cfg.wavelengthsPath)

        if self.mode == 'VNIR':
            return wavelengths['wavelength_vs'].flatten()
        elif self.mode == 'Fluor':
            return wavelengths['wavelength_fl'].flatten()
        elif self.mode == 'SWIR':
            return wavelengths['wavelength_ir'].flatten()[16:132]
        else:
            return None

    def getTrainTest(self, dataDF, fold):
        '''
        :param dataDF: data frame generated based on scanning method (for ex. VNIR_DF)
        :param fold: fold number
        :return: this function is a utility to organize dataset and return the arranged data frame
        '''
        # Read list of caseIDs in the test set
        testFoldsDF = pd.read_csv(os.path.join(cfg.dataFolder, cfg.foldsFile))
        testIDs = ['USDA' + x for x in testFoldsDF['Test_' + str(fold)].dropna().tolist()]

        # Extract train and test data frames
        testDF = dataDF[dataDF['caseID'].isin(testIDs)].reset_index(drop=True)
        trainDF = dataDF[~dataDF['caseID'].isin(testIDs)].reset_index(drop=True)

        # Remove species from train set not represented in test set
        # TODO: use transfer learning/fine tuning to consider all species in train set
        goodSpecies = np.unique(testDF['DNA'])
        trainDF = trainDF[trainDF['DNA'].isin(goodSpecies)].reset_index(drop=True)
        return trainDF, testDF

    def getTrainTestDict(self):
        '''
        :return: generates folds based on K value specified in config file out of dataframes.
        Each scanning method will have each own key in data directory
        '''
        VNIR_DF, Fluor_DF, SWIR_DF = getData()
        trainTestDict = {}
        for f in range(cfg.nFolds):
            fold = f + 1
            foldName = 'Fold' + str(fold)
            trainTestDict[foldName] = {}
            trainTestDict[foldName]['VNIR_trainDF'], trainTestDict[foldName]['VNIR_testDF'] = getTrainTest(VNIR_DF,
                                                                                                           fold)
            trainTestDict[foldName]['Fluor_trainDF'], trainTestDict[foldName]['Fluor_testDF'] = getTrainTest(Fluor_DF,
                                                                                                             fold)
            trainTestDict[foldName]['SWIR_trainDF'], trainTestDict[foldName]['SWIR_testDF'] = getTrainTest(SWIR_DF,
                                                                                                           fold)
            return trainTestDict


