from sklearn import svm
from scipy.cluster.vq import whiten
import numpy as np
from separate_train_test import separate_train_test

SHOULD_WHITEN = True #always whiten for svms
KERNEL_TYPE = 'linear'
#INTERCEPT = 2

'''
Input your training data and get a trained SVM.
Assume that by here everything has been whitened.
'''
def getTrainedSVM(classes_train):
    trainMatrix = []
    labels = []

    for i in range(len(classes_train)):
        genre_train = classes_train[i]
        for featureVector in genre_train:
            trainMatrix.append(featureVector)
            labels.append(i)

    songsvm = svm.SVC(kernel=KERNEL_TYPE)
    print "Kernel type: ", KERNEL_TYPE
##    dec = songsvm.decision_function([[1]])
##    print "shape should be 6. ", dec.shape[1]
##    assert( dec.shape[1] == len(classes_train)*(len(classes_train)-1)/2)
    print songsvm
    #songsvm = svm.LinearSVC()
    print "training svm on ", len(trainMatrix), " feature vectors."
    songsvm.fit(trainMatrix, labels)
    return songsvm

'''Use distance from decision boundary as a confidence measure.'''
def classifyConfidence(songVectors, classifier):
    total = 0
    for songVector in songVectors:
        total+= classifier.decision_function(songVector)[0]
    netPrediction = 0 if total <0 else 1
    return netPrediction

'''Predict the class that the majority of feature vectors are'''
def classifyMajority(songVectors, num_classes, classifier):
    guesses = [0]*num_classes
    for songVector in songVectors:
        guess = classifier.predict(songVector)
        guesses[guess[0]]+=1
        
    '''Return the most popular guess.'''
    return guesses.index(max(guesses))

def classify(songVectors, num_classes, classifier, classificationMethod):
    if classificationMethod == 'majority':
        return classifyMajority(songVectors, num_classes, classifier)
    elif classificationMethod=='confidence':
        assert(False), "Confidence not implemented for Multiclass classification-- use majority."
    else:
        assert(False), "Invalid classification method proposed."
        
'''Each interval is a song'''    
def getSingleClassAccuracy(testclass, intervals, num_classes, classifier, classificationMethod):
    classifications = [0]*num_classes
    for start, end in intervals:
        songVectors = testclass[start:end]
        predictions = classify(songVectors, num_classes, classifier, classificationMethod)
        classifications[predictions]+=1
        
    return classifications
            
def getClassifierAccuracy(classes_test, classes_intervals, classifier, classificationMethod):
    num_classes = len(classes_test)
    
    confusionMatrix = []
    assert(len(classes_intervals)==len(classes_test))
    for i in range(len(classes_test)):
        genre_test = classes_test[i]
        genre_intervals = classes_intervals[i]
        row = getSingleClassAccuracy(genre_test, genre_intervals, num_classes, classifier, classificationMethod)
        confusionMatrix.append(row)
                                     
    return confusionMatrix

# def separate_trainTest(myclass, fraction_training, startEnd):
#     num_train_songs = int(len(startEnd)*fraction_training)
#     num_train_vectors = startEnd[num_train_songs][0]
#     myclass_train = myclass[:num_train_vectors]
#     myclass_test = myclass[num_train_vectors:]

#     '''To update the intervals to be correct on the test set,
#     1) only store those that are relevant to  the test set,
#     2) Reduce all start, end points by num_train_vectors so they
#     index properly into myclass_test. '''
#     intervalsTest = startEnd[num_train_songs:]
#     for i in range(len(intervalsTest)):
#         intervalsTest[i][0]-=num_train_vectors
#         intervalsTest[i][1]-=num_train_vectors
        
#     return myclass_train, myclass_test, intervalsTest

# def whitenData(allGenresWindows):
#     flatWindows = []
#     for genreWindows in allGenresWindows:
#         flatWindows+= genreWindows
    
#     whitened_features = whiten(np.array(flatWindows))
#     allGenresWhitened = []
#     start = 0
#     for genreWindows in allGenresWindows:
#         end = start + len(genreWindows)
#         allGenresWhitened.append(whitened_features[start:end])
#         start = end
#     return allGenresWhitened

def run_svm(allGenresWindows, allGenresStartEnd, fraction_training, classificationMethod):
    classes_train, classes_test, classes_intervals = separate_train_test(allGenresWindows, allGenresStartEnd, fraction_training, SHOULD_WHITEN)
    classifier = getTrainedSVM(classes_train)
    confusionMatrix = getClassifierAccuracy(classes_test, classes_intervals, classifier, classificationMethod)
    return confusionMatrix    