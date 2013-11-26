from textureWindows import getAllTextureWindows
from getTrainingData import getTrainingData
from reader import Song
from run_svm import run_svm
import random
import sys

WINDOW_WIDTH_SECONDS = 1
RANDOM_FRACTION = .03 #What portion of the song do you use-- all of it or just some?
FRACTION_TRAINING = .7
CLASSIFICATION_METHOD = 'majority' #'confidence

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

##class2_windows = [item[1:24] for item in class2_windows] THESE TWO LINES NOT MADE TO BE MULTICLASS YET
##class1_windows = [item[1:24] for item in class1_windows]

'''confusionMatrix[i] gives a list showing how things that are actually genre classNames[i] were classified,
ie if confusionMatrix[i][i] has everything, then the genre classNames[i] was classified perfectly all the time.'''
confusionMatrix = run_svm(allGenresWindows, allGenresStartEnd, FRACTION_TRAINING, CLASSIFICATION_METHOD)
for row in confusionMatrix:
    print row
