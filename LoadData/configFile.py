import os

# Data folder
dataFolder = r'D:\FishData\PanteaTables'

# Wavelengths file location
wavelengthsPath = r'D:\FishData\data_fish_wavelength.mat'

# Results folder
resultsFolder = r'D:\Fish_Fillet_Codes\python_code\outputs'

# Plots folder
plotsFolder = r'D:\Fish_Fillet_Codes\python_code\outputs\plots'

# Number of folds
nFolds = 4

# Folds file
foldsFile = 'testSet_4_25species.csv'

# species to exclude
dropSpecies = [] #['Sand Sole', 'Porgy (Stenotomus sp.)', 'Coho salmon', 'Rooster hind', 'Black sea bass', 'Giant perch']

# Size of pixel windows
windowSz = 10

# Buffer near beginning and end of spectra (in numbers of bands) 
spectrumBuffer = 5

# Minimum separation between selected wavelengths
minSep = 2

# Normalization type
normType = 'fluorNorm'

# Experiment and trial info
trialName = 'SimAnneal'
experiment = 'AccuracyAsFitness'
classifier = 'wknn'

# Output folder
outFolder = os.path.join(resultsFolder, trialName, classifier)