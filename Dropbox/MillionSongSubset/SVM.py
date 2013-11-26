from sklearn import svm
from TrainingDataExtractor import getData
from scipy.cluster.vq import whiten
import numpy as np
from copy import deepcopy

def getTrainedSVM(rockTrain, jazzTrain):
    trainMatrix = []
    labels = []

    #0 is rock, 1 is jazz
    for featureVector in rockTrain:
        trainMatrix.append(featureVector)
        labels.append(ROCK_LABEL)

    for featureVector in jazzTrain:
        trainMatrix.append(featureVector)
        labels.append(JAZZ_LABEL)

    songsvm = svm.LinearSVC()
    print "training svm on ", len(trainMatrix), " feature vectors."
    songsvm.fit(trainMatrix, labels)
    return songsvm

def classify(song, classifier):
    total = 0
    #record= []
    for featureVector in song.featureVectors:
        prediction = classifier.decision_function(featureVector)[0] #the confidence value
        total+=prediction
        #record.append(prediction)
    #negative means 0 means rock, positive means 1 means jazz
    #print "total: ", total, "\nrecord: ", record
    netPrediction = 0 if total <0 else 1
    return netPrediction

def getClassifierAccuracy(rockTest, jazzTest, classifier):
    rockRight = 0
    rockWrong = 0
    jazzRight = 0
    jazzWrong = 0
    
    for song in rockTest:
        if classify(song, classifier)==ROCK_LABEL:
            rockRight+=1
        else:
            rockWrong+=1

    for song in jazzTest:
        if classify(song, classifier)==JAZZ_LABEL:
            jazzRight+=1
        else:
            jazzWrong+=1

    return rockRight, rockWrong, jazzRight, jazzWrong

def getFeatures(songList):
    features=[]
    for song in songList:
        for vector in song.featureVectors:
            features.append(vector)
    return features

def updateSongs(whitenedFeatures, originalSongs):
    whitenedSongs = deepcopy(originalSongs)
    curr = 0
    for songIndex in range(len(originalSongs)):
        numFeatures = len(originalSongs[songIndex].featureVectors)
        newFeatures = whitenedFeatures[curr:curr+numFeatures]
        whitenedSongs[songIndex].featureVectors = newFeatures
        curr = curr + numFeatures
    return whitenedSongs

ROCK_LABEL = 0
JAZZ_LABEL = 1

numTotal = 100
numTrain = 80

rocksongs, jazzsongs = getData(numTotal)

##allsongs_whitened = whiten(np.array(rocksongs+jazzsongs))
##whiterocksongs = allsongs_whitened[:len(rocksongs)]
##whitejazzsongs = allsongs_whitened[len(rocksongs):]

rockTrain = rocksongs[:numTrain]
jazzTrain = jazzsongs[:numTrain]
rockTest = rocksongs[numTrain:]
jazzTest = jazzsongs[numTrain:]

rockTrainFeatures = getFeatures(rockTrain)
rockTestFeatures = getFeatures(rockTest)
jazzTrainFeatures = getFeatures(jazzTrain)
jazzTestFeatures = getFeatures(jazzTest)

whitened_features = whiten(np.array(rockTrainFeatures+rockTestFeatures+jazzTrainFeatures+jazzTestFeatures))

endRockTrain = len(rockTrainFeatures)
endRockTest = endRockTrain+len(rockTestFeatures)
endJazzTrain = endRockTest+len(jazzTrainFeatures)
endJazzTest = endJazzTrain+len(jazzTestFeatures)
    
whiteRockTrain = whitened_features[:len(rockTrainFeatures)]
whiteRockTest = whitened_features[endRockTrain:endRockTest]
whiteJazzTrain = whitened_features[endRockTest:endJazzTrain]
whiteJazzTest = whitened_features[endJazzTrain:endJazzTest]

whiteRockTestSongs = updateSongs(whiteRockTest, rockTest)
whiteJazzTestSongs = updateSongs(whiteJazzTest, jazzTest)

assert( len(rockTrainFeatures) == len(whiteRockTrain))
assert( len(rockTestFeatures) == len(whiteRockTest))
assert( len(jazzTrainFeatures) == len(whiteJazzTrain))
assert( len(jazzTestFeatures) == len(whiteJazzTest))

print "Getting Classifier"
classifier = getTrainedSVM(whiteRockTrain, whiteJazzTrain)

print "Validating accuracy"
rockRight, rockWrong, jazzRight, jazzWrong = getClassifierAccuracy(whiteRockTestSongs, whiteJazzTestSongs, classifier)
print "rockRight: ", rockRight
print "rockWrong: ", rockWrong
print "jazzRight: ", jazzRight
print "jazzWrong: ", jazzWrong




        
    

