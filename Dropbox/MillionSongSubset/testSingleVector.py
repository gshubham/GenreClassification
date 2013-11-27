'''This file should be called to do the testing
where each song will be associated with *one* 
feature vector. This is in contrast with the 
previous ones, where songs were the sum of many
predictions on many individual/smaller feature 
vectors.'''

from getTrainingData import getTrainingData
from chordFeatures import extractChordFeatures
from svm_single import svm_single
from reader import Song

NUM_TRAINING_EXAMPLES = 100
FRACTION_TRAINING = .7
GENRES_USED = ['metal', 'jazz']#,  'hiphop','rock', 'pop']

allGenresSongs = getTrainingData(GENRES_USED, NUM_TRAINING_EXAMPLES)
allGenresVectors = []
for genreSongs in allGenresSongs:
	genreVectors = []
	for song in genreSongs:
		vector = extractChordFeatures(song)
		genreVectors.append(vector)
	allGenresVectors.append(genreVectors)

confusionMatrix = svm_single(allGenresVectors, FRACTION_TRAINING)
for row in confusionMatrix:
	print row

