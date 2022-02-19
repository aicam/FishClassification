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

    def getTrainTestFold(self, dataDF, fold):
        '''
        :param dataDF: data frame generated based on scanning method (for ex. VNIR_DF)
        :param fold: fold number
        :return: this function is a utility to organize dataset and return the arranged data frame by fold number
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

    def assembleDF(self, data):
        '''
        loadmat returns a dictionary which every column in .mat file is mapped to a new key in the dictionary.
        This dictionary is the base data used in this method to generate pandas dataframe to work with data much easier
        :param data: loadmat generated dictionary
        :return: pandas dataframe
        '''
        # Build data frame
        X = np.matrix(data['X'])
        dataDF = pd.DataFrame(X, columns=['X' + str(x + 1) for x in range(X.shape[1])])

        # # Normalize
        # if doNorm:
        #     dataDF = normalize(dataDF, mode)

        # Add caseID and DNA columns
        dataDF['caseID'] = [x.strip() for x in data['caseID'].astype(str)]
        dataDF['DNA'] = [x.strip() for x in data['DNA'].astype(str)]

        # Add row and col if they exist
        if 'row' in data and 'col' in data:
            dataDF['row'] = data['row'].astype(int)
            dataDF['col'] = data['col'].astype(int)

        # Remove bad fillets
        dataDF = dataDF.loc[dataDF.DNA != ""]

        # Remove excluded species
        dataDF = dataDF[~dataDF['DNA'].isin(cfg.dropSpecies)]

        return dataDF

    def getData(self):
        '''
        :return: generate dataset dataframe based on scanning method
        '''
        # Load data by loadmat (default mat loader in SciPy)
        # loadmat returns a dictionary
        data_VNIR = loadmat(os.path.join(cfg.dataFolder, 'tbl_vis_with_coords_converted.mat'))
        data_Fluor = loadmat(os.path.join(cfg.dataFolder, 'tbl_FL_with_coords_converted.mat'))
        data_SWIR = loadmat(os.path.join(cfg.dataFolder, 'tbl_SWIR_with_coords_converted.mat'))

        # Load data into DataFrames
        VNIR_DF = self.assembleDF(data_VNIR)
        Fluor_DF = self.assembleDF(data_Fluor)
        SWIR_DF = self.assembleDF(data_SWIR)

        return VNIR_DF, Fluor_DF, SWIR_DF

    def getTrainTestDict(self):
        '''
        :return: generates folds based on K value specified in config file out of dataframes.
        Each scanning method will have each own key in data directory
        '''
        VNIR_DF, Fluor_DF, SWIR_DF = self.getData()
        trainTestDict = {}
        for f in range(cfg.nFolds):
            fold = f + 1
            foldName = 'Fold' + str(fold)
            trainTestDict[foldName] = {}
            trainTestDict[foldName]['VNIR_trainDF'], trainTestDict[foldName]['VNIR_testDF'] = self.getTrainTestFold(VNIR_DF,
                                                                                                                    fold)
            trainTestDict[foldName]['Fluor_trainDF'], trainTestDict[foldName]['Fluor_testDF'] = self.getTrainTestFold(
                Fluor_DF,
                fold)
            trainTestDict[foldName]['SWIR_trainDF'], trainTestDict[foldName]['SWIR_testDF'] = self.getTrainTestFold(SWIR_DF,
                                                                                                                    fold)
            return trainTestDict
