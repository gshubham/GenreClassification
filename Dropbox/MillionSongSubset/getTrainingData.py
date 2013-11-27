import pickle
from reader import Song
FOLDER = "pickled_training/"

def getTrainingData(classNames, numExamples):
	if not (numExamples==100 or numExamples==200):
		assert(False), "Only 100 or 200 examples supported"

	allClassSongs = []
	for className in classNames:
		print "unpickling ", className
		classFile = open(FOLDER+className+'songs_nofilter_'+str(numExamples)+'.pkl', 'rb')
		classSongs = pickle.load(classFile)
		classFile.close()
		allClassSongs.append(classSongs)
	return allClassSongs

   
   
