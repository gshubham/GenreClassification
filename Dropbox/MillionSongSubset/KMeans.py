import h5py
import os
import random
import numpy as np
#import scipy
from scipy.cluster.vq import whiten
from scipy.cluster.vq import kmeans
from numpy.linalg import norm
import TrainingDataExtractor


def randomSampleFeatures(song, numSamples):
    chosen = []
    remaining = len(song.featureVectors)
    for i in range(len(song.featureVectors)):
        prob = numSamples/float(remaining)
        if random.random()<prob:
            chosen.append(song.featureVectors[i])
            numSamples-=1
        remaining-=1
    return chosen

'''todo: make it so you return numVectors exactly.
As it is, it returns a number <= numVectors, basically
that number rounded down to be a multiple of numSongs.'''

def getFeatureVectors(songs, numVectors):
    perSong = numVectors/(len(songs))
    featureVectors = []
    for song in songs:
        featureVectors+=randomSampleFeatures(song, perSong)
    return featureVectors

def getCentroids(trainingSongs, num_centroids):
    
    total_feature_vectors = 3000

    songfeatures = getFeatureVectors(trainingSongs, total_feature_vectors)
    songfeatures_ndarray = np.array(songfeatures)
    '''Whitening divides each feature by its std-dev to give unit variance.
    This is a necessary step before doing the scipy k-means.
    Note that to classify new  training examples, I'll need to
    normalize those input features with the same ratios which I'll need to
    calculate.
    '''
    song_whitened = whiten(songfeatures_ndarray)
    ratios =  songfeatures_ndarray[0] / song_whitened[0]
    song_codebook, song_distortion = kmeans(song_whitened, num_centroids)
    centroids = song_codebook * ratios
    return centroids, song_distortion



def getFeatureError(vector, centroids):
    return min(norm(vector- centroid, 2) for centroid in centroids)

def getSongError(song, centroids):
    total = 0
    for vector in song.featureVectors:
        error = getFeatureError(vector, centroids)
        total+=error
    return total
        
def classify(song, firstCentroids, secondCentroids):
    e1 = getSongError(song, firstCentroids)
    e2 = getSongError(song, secondCentroids)
    if e1<e2:
        return 'first'
    else:
        return 'second'

def getValidationError(firstTest, secondTest, firstCentroids, secondCentroids):
    firstRight = 0
    firstWrong = 0
    secondRight = 0
    secondWrong = 0
    for song in firstTest:
        if classify(song, firstCentroids, secondCentroids)=='first':
            firstRight+=1
        else:
            firstWrong+=1
    for song in secondTest:
        if classify(song, firstCentroids, secondCentroids)=='second':
            secondRight+=1
        else:
            secondWrong+=1
    return firstRight, firstWrong, secondRight, secondWrong

def findModel(numCentroids):

    print "/n/nNEW TESTING ROUND WITH ", numCentroids, "CENTROIDS"
    print "GETTING CENTROIDS: ROCK"
    rock_centroids, rock_distortion = getCentroids(trainRock, numCentroids)
    print "GETTING CENTROIDS: JAZZ"
    jazz_centroids, jazz_distortion = getCentroids(trainJazz, numCentroids)


    print "TESTING"
    jazzRight, jazzWrong, rockRight, rockWrong = getValidationError(testJazz, testRock, jazz_centroids, rock_centroids)
    print "jazzRight: ", jazzRight
    print "jazzWrong: ", jazzWrong
    print "rockRight: ", rockRight
    print "rockWrong: ", rockWrong
    
rocksongs, jazzsongs = TrainingDataExtractor.getData(100)
trainRock = rocksongs[:70]
testRock = rocksongs[70:]
trainJazz = jazzsongs[:70]
testJazz = jazzsongs[70:]

findModel(5)
findModel(10)
findModel(20)
findModel(40)





##def normalize(data):
##    highestVals = []
##    lowestVals = []
##    for i in range(len(data[0])):
##        high = max(item[i] for item in data)
##        low = min(item[i] for item in data)
##        highestVals.append(high)
##        lowestVals.append(low)
##
##    
##    normalized = []
##    for vector in data:
##        normvec = [(vector[i] - lowestVals[i])/float(highestVals[i]-lowestVals[i]) for i in range(len(data[0]))]
##        normalized.append(normvec)
##
##    return normalized





        
        

