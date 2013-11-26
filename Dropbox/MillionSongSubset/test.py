from textureWindows import getAllTextureWindows
from getTrainingData import getTrainingData
from reader import Song
from run_svm import run_svm
import random
import sys

WINDOW_WIDTH_SECONDS = 1
RANDOM_FRACTION = .1 #What portion of the song do you use-- all of it or just some?
FRACTION_TRAINING = .7
CLASSIFICATION_METHOD = 'majority' #'confidence

# class1 = 'metal'
# class2 = 'pop'
class1 = sys.argv[1]
class2 = sys.argv[2]


class1Songs, class2Songs = getTrainingData(class1, class2)

print "Done getting training data, now extracting texture windows"

'''class2_windows is a list of windows/vectors from the songs.
startEndclass2 associates songs with the start/end of its window, ie
the ith song has in the ith slot of startEndclass2 a tuple specifying the
start index (inclusive) and end index (exclusive) for that song.'''
class1_windows, startEndclass1 = getAllTextureWindows(class1Songs, WINDOW_WIDTH_SECONDS, RANDOM_FRACTION)
class2_windows, startEndclass2 = getAllTextureWindows(class2Songs, WINDOW_WIDTH_SECONDS, RANDOM_FRACTION)

##class2_windows = [item[1:24] for item in class2_windows]
##class1_windows = [item[1:24] for item in class1_windows]

class1_accuracy, class2_accuracy = run_svm(class1_windows, class2_windows, startEndclass1, startEndclass2, FRACTION_TRAINING, CLASSIFICATION_METHOD)
print "class1: ", class1_accuracy
print "class2: ", class2_accuracy
