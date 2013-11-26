from textureWindows import getAllTextureWindows
from getTrainingData import getTrainingData
from reader import Song
from run_svm import run_svm
import random

WINDOW_WIDTH_SECONDS = 1
RANDOM_FRACTION = .05 #What portion of the song do you use-- all of it or just some?
FRACTION_TRAINING = .7
CLASSIFICATION_METHOD = 'confidence' #'confidence


metalSongs, jazzSongs = getTrainingData()


##########TESTING###########
##song = jazzSongs[0]
##song.featureVectors = [[1,1], [2,2], [3,3]]
##song.startTimes = [0, .1, 1.2]
##
##song2 = jazzSongs[1]
##song2.featureVectors = [[1,1], [0,0], [3,3], [4,4]]
##song2.startTimes = [0, .1, .15, 1.2]
##
##songs = [song, song2]
##testWindows, startEnd = getAllTextureWindows(songs, 1, 1)
##
##assert(False)
#########DONE TESTING#########

print "Done getting training data, now extracting texture windows"

'''jazz_windows is a list of windows/vectors from the songs.
startEndJazz associates songs with the start/end of its window, ie
the ith song has in the ith slot of startEndJazz a tuple specifying the
start index (inclusive) and end index (exclusive) for that song.'''
jazz_windows, startEndJazz = getAllTextureWindows(jazzSongs, WINDOW_WIDTH_SECONDS, RANDOM_FRACTION)
metal_windows, startEndMetal = getAllTextureWindows(metalSongs, WINDOW_WIDTH_SECONDS, RANDOM_FRACTION)

##jazz_windows = [item[1:24] for item in jazz_windows]
##metal_windows = [item[1:24] for item in metal_windows]

jazz_accuracy, metal_accuracy = run_svm(jazz_windows, metal_windows, startEndJazz, startEndMetal, FRACTION_TRAINING, CLASSIFICATION_METHOD)
print "jazz: ", jazz_accuracy
print "metal: ", metal_accuracy
