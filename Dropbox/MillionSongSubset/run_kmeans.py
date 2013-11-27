from separate_train_test import separate_train_test
from scipy.cluster.vq import kmeans
from numpy.linalg import norm
from config import *
# SHOULD_WHITEN = True
# ERROR_POWER = 1;

def train_genre_model(genre_vectors, num_centroids):
	centroids, distortion = kmeans(genre_vectors, num_centroids)
	return centroids, distortion 

def get_genres_models(genres_train, num_centroids):
	genres_models = []
	genres_distortions = []
	for genre_vectors in genres_train:
		model, distortion = train_genre_model(genre_vectors, num_centroids)
		genres_models.append(model)
		genres_distortions.append(distortion)
	return genres_models, genres_distortions

def distance_nearest_centroid(song_vector, model):
	'''Get the 2-norm distance to the nearest cluster'''
	return min(norm(song_vector - centroid, 2) for centroid in model)**ERROR_POWER

def get_model_error(song_vectors, model):
	total_error = 0
	for song_vector in song_vectors:
		error = distance_nearest_centroid(song_vector, model)
		total_error+=error
	return total_error

def classify(song_vectors, models, num_classes):
	errors = [0]*num_classes
	for i in range(len(models)):
		model = models[i]
		error = get_model_error(song_vectors, model)
		errors[i]=error

	'''Return the lowest-error model'''
	return errors.index(min(errors)) 

def get_single_genre_accuracy(vectors, intervals, models, num_classes):
	classifications = [0]*num_classes
	for start, end in intervals:
		song_vectors = vectors[start:end]
		prediction = classify(song_vectors, models, num_classes)
		classifications[prediction]+=1

	return classifications

def get_classifier_accuracy(genres_test, genres_intervals, genres_models):
	num_classes = len(genres_test)
	confusionMatrix = []
	for i in range(len(genres_test)):
		genre_vectors = genres_test[i]
		genre_interval = genres_intervals[i]
		row = get_single_genre_accuracy(genre_vectors, genre_interval, genres_models, num_classes)
		confusionMatrix.append(row)

	return confusionMatrix

'''
Model for kmeans:
- run one kmeans for each genre on the training vectors and get the centroids
- for classification, take each vector in a song, assign to the nearest centroid, 
then take the sum of the distances is the error. Assign it to the model with the 
minimal error.
'''
def run_kmeans(genres_vectors, genres_start_end, fraction_training, num_centroids):
	genres_train, genres_test, genres_intervals = separate_train_test(genres_vectors, genres_start_end, fraction_training, SHOULD_WHITEN)
	genres_models, genres_distortions = get_genres_models(genres_train, num_centroids)
	print "Distortions: "
	print genres_distortions
	confusionMatrix = get_classifier_accuracy(genres_test, genres_intervals, genres_models)
	return confusionMatrix
