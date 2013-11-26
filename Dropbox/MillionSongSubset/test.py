from textureWindows import getAllTextureWindows
from getTrainingData import getTrainingData
from reader import Song
from run_svm import run_svm
from run_kmeans import run_kmeans
import random
import sys

WINDOW_WIDTH_SECONDS = 1
RANDOM_FRACTION = .05 #What portion of the song do you use-- all of it or just some?
FRACTION_TRAINING = .7
SVM_CLASSIFICATION_METHOD = 'majority' #'confidence #for run_svm
KMEANS_NUM_CENTROIDS = 1
CLASSIFIER_TYPE = "svm"

classNames = ['metal', 'jazz', 'pop', 'hiphop', 'rock']

allGenresSongs = getTrainingData(classNames)

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

for row in confusionMatrix:
    print row
