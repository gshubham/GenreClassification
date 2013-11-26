import pickle
from reader import Song

def getTrainingData(classNames):
    allClassSongs = []
    for className in classNames:
        print "unpickling ", className
        classFile = open(className+'songs_nofilter.pkl', 'rb')
        classSongs = pickle.load(classFile)
        classFile.close()
        allClassSongs.append(classSongs)
    return allClassSongs

   
   
