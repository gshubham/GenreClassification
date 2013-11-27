from sklearn import svm
from scipy.cluster.vq import whiten
import numpy as np

KERNEL_TYPE = "linear"

def getTrainedSVM(allGenresTrain):
	trainMatrix = []
	labels = []
	for i in range(len(allGenresTrain)):
		label = i 
		genre_vectors = allGenresTrain[i]
		trainMatrix+=genre_vectors
		labels+=[i]*len(genre_vectors)

	songsvm = svm.SVC(kernel=KERNEL_TYPE)
	print "Kernel type: ", KERNEL_TYPE
	print songsvm
	print "training svm on ", len(trainMatrix), " feature vectors."
	songsvm.fit(trainMatrix, labels)
	return songsvm

def separateTrainTest(allGenresVectors, fraction_training):
	allGenresTrain = []
	allGenresTest = []
	for genreVectors in allGenresVectors:
		cutoff = int(len(genreVectors)*fraction_training)
		train = genreVectors[:cutoff]
		test = genreVectors[cutoff:]
		allGenresTrain.append(train)
		allGenresTest.append(test)
	return allGenresTrain, allGenresTest

def getSingleClassAccuracy(test_vectors, num_classes, classifier):
	classifications = [0]*num_classes
	for vector in test_vectors:
		prediction = classifier.predict(vector)[0] 
		classifications[prediction]+=1

	return classifications
def getAccuracy(allGenresTest, classifier):
	num_classes = len(allGenresTest)

	confusionMatrix = []
	for i in range(len(allGenresTest)):
		genre_test = allGenresTest[i]
		row = getSingleClassAccuracy(genre_test, num_classes, classifier)
		confusionMatrix.append(row)
	                                 
	return confusionMatrix

def whitenData(allGenresVectors):
	allvectors = []
	for genreVectors in allGenresVectors:
		allvectors+=genreVectors

	whitened_vectors = allvectors#whiten(np.array(allvectors))
	whitened_genres = []

	start = 0
	for genreVectors in allGenresVectors:
		end = start + len(genreVectors)
		whitened_genres.append(whitened_vectors[start:end])
		start = end
	return whitened_genres

def svm_single(allGenresVectors, fraction_training):
	allGenresWhitened = whitenData(allGenresVectors)
	allGenresTrain, allGenresTest = separateTrainTest(allGenresWhitened, fraction_training)
	classifier = getTrainedSVM(allGenresTrain)
	confusionMatrix = getAccuracy(allGenresTest, classifier)
	return confusionMatrix
