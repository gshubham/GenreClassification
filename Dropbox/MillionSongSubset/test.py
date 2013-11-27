from textureWindows import getAllTextureWindows
from getTrainingData import getTrainingData
from reader import Song
from run_svm import run_svm
from run_kmeans import run_kmeans
import random
import sys

from config import *

# WINDOW_WIDTH_SECONDS = .01
# RANDOM_FRACTION = .1 #What portion of the song do you use-- all of it or just some?
# FRACTION_TRAINING = .7
# SVM_CLASSIFICATION_METHOD = 'majority' #'confidence #for run_svm
# KMEANS_NUM_CENTROIDS = int(sys.argv[1])#1
# CLASSIFIER_TYPE = "kmeans"

# classNames = ['metal', 'jazz',  'hiphop','rock', 'pop']

allGenresSongs = getTrainingData(GENRES_USED, NUM_TRAINING_EXAMPLES)

print "Done getting training data, now extracting texture windows"

'''class_windows is a list of windows/vectors from the songs.
startEndclass associates songs with the start/end of its window, ie
the ith song has in the ith slot of startEndclass a tuple specifying the
start index (inclusive) and end index (exclusive) for that song.'''

allGenresWindows = []
allGenresStartEnd = []
for singleGenreSongs in allGenresSongs:
    singleGenreWindows, singleGenreStartEnd = getAllTextureWindows(singleGenreSongs, WINDOW_WIDTH_SECONDS, RANDOM_FRACTION)
    allGenresWindows.append(singleGenreWindows)
    allGenresStartEnd.append(singleGenreStartEnd)

############## ABOVE: EXTRACTING THE FEATURES ##############
############## BELOW: TRAINING THE CLASSIFIER ##############


    
'''confusionMatrix[i] gives a list showing how things that are actually genre classNames[i] were classified,
ie if confusionMatrix[i][i] has everything, then the genre classNames[i] was classified perfectly all the time.'''

if CLASSIFIER_TYPE == 'svm':
    confusionMatrix = run_svm(allGenresWindows, allGenresStartEnd, FRACTION_TRAINING, SVM_CLASSIFICATION_METHOD)
    
elif CLASSIFIER_TYPE == 'kmeans':
    confusionMatrix = run_kmeans(allGenresWindows, allGenresStartEnd, FRACTION_TRAINING, KMEANS_NUM_CENTROIDS)
else:
    assert(False), 'INVALID CLASSIFIER TYPE. (Only "svm" and "kmeans" supported.)'

# print "\nGenres: ", GENRES_USED
# print "NumCentroids", KMEANS_NUM_CENTROIDS

'''Print the config variables'''
import config
for varname in config.__dict__.keys():
	if varname[0:2]!="__":
		print varname, config.__dict__[varname]

print "Confusion Matrix:"
for row in confusionMatrix:
    print row
