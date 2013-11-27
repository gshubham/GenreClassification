import h5py
import os
import math
import pickle
import numpy as np
from copy import deepcopy
#from Song import Song
## import matplotlib.pyplot as plt

#segments_confidence
class Centroid:
    def __init__(self, fname):
        self.fname = fname
        self.dimensionLength = 12
        self.meanVector = self.getMeanVector()
        self.covarianceMatrix = self.getCovarianceMatrix()


    def getMeanVector(self):
        meanVector = []
        for i in range(0, self.dimensionLength):
            meanVector.append(0.0)
        return meanVector

    def getCovarianceMatrix(self):
        covarianceMatrix = []
        for i in range(0, self.dimensionLength):
            covarianceMatrix.append([])
            for j in range(0, self.dimensionLength):
                covarianceMatrix[i].append(0.0)
        return covarianceMatrix
    def addtoMeanVector(self, secondaryVector):
        for i in range(len(secondaryVector)) :
            self.meanVector[i] += secondaryVector[i]

    def addtoCovarianceMatrix(self, covarianceMatrix):
        for i in range(0, self.dimensionLength):
            for j in range(0, self.dimensionLength):
                self.covarianceMatrix[i][j] += covarianceMatrix[i][j]

    def averageMeanVector(self, num):
        for i in range(len(self.meanVector)) :
            self.meanVector[i] = float(self.meanVector[i]/num);

    def averageCovarianceMatrix(self, num):
        for i in range(0, self.dimensionLength):
            for j in range(0, self.dimensionLength):
                self.covarianceMatrix[i][j] = float(self.covarianceMatrix[i][j]/num);

class Song:
    def __init__(self, fname, needJazz, needRock):
        try:
            f = h5py.File(fname, 'r')
        except Exception, e:
            self.featureVectors = []
            self.genre = 'neither'
            return
        self.fname = fname
        self.tags = self.getTags(f)
        self.genre = self.getGenre(self.tags)
        if self.genre=='neither':
            f.close()
            return
        if self.genre=='jazz' and not needJazz:
            f.close()
            return
        if self.genre=='rock' and not needRock:
            f.close()
            return
        self.featureVectors, self.confidences = self.getFeatureVectorsAndConf(f)
        self.startTimes = self.getStartTimes(f)
        if(len(self.featureVectors) ==  0) :
            f.close()
            return
        self.meanVector = self.getMeanVector()
        self.covarianceMatrix = self.getCovarianceMatrix()
        f.close()
        #self.confidences = self.getConfidences(f)
        
        #self.avgMFCC, self.maxMFCC, self.minMFCC = self.getAvgMFCC(f)
        #print "done constructing"
        #read in the song here.
        #Attributes: genre, fname, avgs for each mfcc

    def getFeatureVectorsAndConf(self, f):
        mfcc2d = f['analysis']['segments_timbre']
        confidences = f['analysis']['segments_confidence']
        
        confValues = []
        featureVectors = []
        
        for i in range(len(mfcc2d)):
            conf = confidences[i]
            # if conf<.6:
            #     continue
            item = mfcc2d[i]
            confValues.append(conf)
            featureVectors.append(item)
            
        return featureVectors, confValues

##    def getConfidences(self, f):
##        
##        confidences = f['analysis']['segments_confidence']
##        confValues = []
##        for confidence in confidences:
##            confValues.append(confidence)
##        return confValues
        
    def getTags(self, f):
        tags = f['metadata']['artist_terms']
        alltags = []
        for tag in tags:
            alltags.append(tag)
        return alltags

    def getStartTimes(self, f):
        startTimes = []
        confidences = f['analysis']['segments_confidence']
        start = f['analysis']['segments_start']
        for i in range(len(start)):
            conf = confidences[i]
            # if conf<.6:
            #     continue
            startTimes.append(start[i])
        return startTimes

    def getGenre(self, tags):
        top5 = tags[:5]
        numjazz = 0
        numrock = 0
        numhip = 0
        numpop = 0
        nummetal = 0
        for tag in top5:
            if 'rock' in tag:
                numrock+=1
            if 'hip hop' in tag:
                numhip+=1
            if 'pop' in tag:
                numpop+=1
            if 'jazz' in tag:
                numjazz+=1
            if 'metal' in tag:
                nummetal+=1
        if numjazz>=1 and nummetal==0 and numrock==0 and numhip==0 and numpop==0:
            return 'jazz'
        if numrock>=1:
            return 'rock'
        return 'neither'

    # def getGenre(self, tags):
    #     print self.tags
    #     genreName = raw_input("Enter category name : ");
    #     if(genreName == "j" or genreName == "ja" or  genreName == "jaz" or genreName == "jazz"):
    #         print genreName
    #         return 'jazz'

    #     if(genreName == "r" or genreName == "ro" or genreName == "roc" or genreName == "rock"):
    #         print genreName
    #         return 'rock'

    #     print genreName
    #     return 'neither'

    def getAvgMFCC(self, f):
        mfcc2d = f['analysis']['segments_timbre']
        confidences = f['analysis']['segments_confidence']
        numsegments = mfcc2d.shape[0]
        numcoeff = mfcc2d.shape[1]
        totalcoeff = [0]*numcoeff
        maxcoeff = [0]*numcoeff
        mincoeff = [0]*numcoeff

        total = 0
        for i in range(len(mfcc2d)):
            conf = confidences[i]
            if conf<.6:
                continue
            total+=1
            segment = mfcc2d[i]
            for i in range(numcoeff):
                totalcoeff[i]+=segment[i]
                maxcoeff[i] = max(maxcoeff[i], segment[i])
                mincoeff[i] = min(mincoeff[i], segment[i])

        avgcoeff = [item/float(total) for item in totalcoeff]

        for i in range(numcoeff):
            avgcoeff[i] = round(avgcoeff[i], 1)
            mincoeff[i] = round(mincoeff[i], 1)
            maxcoeff[i] = round(maxcoeff[i], 1)
            
        return avgcoeff, maxcoeff, mincoeff
    
    def getMeanVector(self):
        meanVector = []
        for i in range(len(self.featureVectors[0])):
            numerator = sum(item[i] for item in self.featureVectors)
            numerator = float(numerator/len(self.featureVectors))
            meanVector.append(numerator)
        return meanVector

    def getExpectedValue(self, vector):
        expVal = sum(vector)
        expVal = float(expVal / len(vector))
        return expVal

    def addtoMeanVector(self, vector):
        for i in range(len(vector)) :
            self.meanVector[i] += vector[i]

    def getCovarianceMatrix(self):
        covarianceMatrix = []
        for i in range(len(self.featureVectors[0])):
            covarianceMatrix.append([]);
            currentVector = []
            for item in self.featureVectors:
                currentVector.append(item[i] - self.meanVector[i])
            for j in range(len(self.featureVectors[0])):
                innerCurrent = currentVector[:]
                for k in range(len(self.featureVectors)):
                    innerCurrent[k] = currentVector[k] * (self.featureVectors[k][j] - self.meanVector[j]);
                covarianceMatrix[i].append(self.getExpectedValue(innerCurrent));
        return covarianceMatrix



def fillSongs(numNeeded):
    rocksongs = []
    jazzsongs = []

    total=0
    songdirtop = "data"
    for subdirtop in os.listdir(songdirtop):
        songdir = songdirtop + "/" + subdirtop
        for subdir in os.listdir(songdir):
            name = songdir + "/"+ subdir
            try:
                directory = os.listdir(name)
                print "Directory is " , directory
            except Exception, e:
                print "Continuing because " + name + " is not a directory"
                continue
            for ssubdir in directory[:20]:
                name2 = name+"/"+ssubdir
                print name2
                try :
                    print "Trying to get stuff"
                    directory2 = os.listdir(name2)
                    print "Internal directory is ", directory2
                    print len(directory2)
                except Exception, e:
                    "Continuing because " + name2 + " is not a directory in 2"
                    continue
                for fname in directory2:
                    fpath = name2+"/"+fname
                    print fpath
                    print min(len(rocksongs), len(jazzsongs))
                    if len(rocksongs)>=numNeeded and len(jazzsongs)>=numNeeded:
                        return rocksongs[:numNeeded], jazzsongs[:numNeeded]
                    needJazz = len(jazzsongs)<numNeeded
                    needRock = len(rocksongs)<numNeeded
                    currsong = Song(fpath, needJazz, needRock)
                    if currsong.genre == 'jazz' and needJazz:
                        if(len(currsong.featureVectors) > 0) :
                            jazzsongs.append(currsong)
                    elif currsong.genre=='rock' and needRock:
                        if(len(currsong.featureVectors) > 0) :
                            rocksongs.append(currsong)
                    
    return rocksongs[:numNeeded], jazzsongs[:numNeeded]

def getData(numPerGenre):
    rocksongs, jazzsongs = fillSongs(numPerGenre)
    assert( len(rocksongs)==numPerGenre and len(jazzsongs)==numPerGenre) #if false then need more data
    return rocksongs, jazzsongs


def normalize(data):
    highestVals = []
    lowestVals = []
    for i in range(len(data[0])):
        high = max(item[i] for item in data)
        low = min(item[i] for item in data)
        highestVals.append(high)
        lowestVals.append(low)

    
    normalized = []
    for vector in data:
        normvec = [(vector[i] - lowestVals[i])/float(highestVals[i]-lowestVals[i]) for i in range(len(data[0]))]
        normalized.append(normvec)

    return normalized

##def smartplot(data):
##    normalized = normalize(data)
##    plt.imshow(normalized, interpolation='none', aspect=3./300)
##    plt.xticks(range(12), ['a','b','c','d','e','f','g','h','i','j','k','l'])
##    plt.jet()
##    plt.colorbar()
##    plt.show()





def getKLDivergence(meanVectorOne, meanVectorTwo, covarianceMatrixOne, covarianceMatrixTwo) :
    meanVecDiff = np.asarray(meanVectorOne) - np.asarray(meanVectorTwo)
    meanVecDiff = np.asmatrix(meanVecDiff)
    matrixOne = np.asmatrix(covarianceMatrixOne)
    matrixTwo = np.asmatrix(covarianceMatrixTwo)
    determinantOne = np.linalg.det(matrixOne)
    determinantTwo = np.linalg.det(matrixTwo)
    if(determinantTwo<=0 or determinantOne<=0):
        return 1000
    termOne = meanVecDiff*matrixTwo.I*meanVecDiff.T
    termTwo = matrixTwo.I*matrixOne
    return (math.log(determinantTwo/determinantOne) + np.trace(termTwo) + termOne[(0,0)] - 12.0)


def KMeans(allSongs, metalsongs, jazzsongs, hiphopsongs, popsongs, rocksongs) :
    clusters = []
    clusters.append(Centroid("Centroid1"))
    clusters.append(Centroid("Centroid2"))
    clusters.append(Centroid("Centroid3"))
    clusters.append(Centroid("Centroid4"))
    clusters.append(Centroid("Centroid5"))
    clusters[0].addtoMeanVector(metalsongs[0].meanVector)
    clusters[0].addtoCovarianceMatrix(metalsongs[0].covarianceMatrix)
    clusters[1].addtoMeanVector(jazzsongs[0].meanVector)
    clusters[1].addtoCovarianceMatrix(jazzsongs[0].covarianceMatrix)
    clusters[2].addtoMeanVector(hiphopsongs[0].meanVector)
    clusters[2].addtoCovarianceMatrix(hiphopsongs[0].covarianceMatrix)
    clusters[3].addtoMeanVector(popsongs[0].meanVector)
    clusters[3].addtoCovarianceMatrix(popsongs[0].covarianceMatrix)
    clusters[4].addtoMeanVector(rocksongs[0].meanVector)
    clusters[4].addtoCovarianceMatrix(rocksongs[0].covarianceMatrix)
    for iter in range(0, 200):
        cumulative = [0,0,0,0,0]
        newclusters = []
        newclusters.append(Centroid("Centroid1"))
        newclusters.append(Centroid("Centroid2"))
        newclusters.append(Centroid("Centroid3"))
        newclusters.append(Centroid("Centroid4"))
        newclusters.append(Centroid("Centroid5"))
        for song in allSongs:
            distance = []
            for centroid in clusters:
                x = getKLDivergence(song.meanVector, centroid.meanVector, song.covarianceMatrix, centroid.covarianceMatrix)
                y = getKLDivergence(centroid.meanVector, song.meanVector, centroid.covarianceMatrix, song.covarianceMatrix)
                if(x != 1000 and y != 1000):
                    distance.append(x+y)
            if(len(distance) == 5) :
                val, idx = min((val, idx) for (idx, val) in enumerate(distance))
                cumulative[idx] += 1
                newclusters[idx].addtoMeanVector(song.meanVector)
                newclusters[idx].addtoCovarianceMatrix(song.covarianceMatrix)
        for i in range(len(newclusters)):
            if(cumulative[i] > 0):
                newclusters[i].averageMeanVector(cumulative[i])
                newclusters[i].averageCovarianceMatrix(cumulative[i])
        clusters = deepcopy(newclusters)

    return clusters


def main():

    # numTotal = 100
    numTrain = 85
    # inp = open('metalsongs_filter.pkl', 'rb')
    # metalsongs = pickle.load(inp)
    # inp.close()
    # inp = open('jazzsongs_filter.pkl', 'rb')
    # jazzsongs = pickle.load(inp)
    # inp.close()
    # inp = open('popsongs_filter.pkl', 'rb')
    # popsongs = pickle.load(inp)
    # inp.close()
    # inp = open('hiphopsongs_filter.pkl', 'rb')
    # hiphopsongs = pickle.load(inp)
    # inp.close()   
    # inp = open('rocksongs_nofilter.pkl', 'rb')
    # rocksongs = pickle.load(inp)
    # inp.close()
    metalsongs, jazzsongs = getData(200)
    output = open('jazzsongs_nofilter_200.pkl', 'wb')
    pickle.dump(jazzsongs, output)
    output.close()
    # # metalsongs, jazzsongs = getData(100)
    # output = open('popsongs_filter_new.pkl', 'wb')
    # pickle.dump(jazzsongs, output)
    # output.close()
    # # output = open('jazzsongs_filter.pk1', 'wb')
    # pickle.dump(jazzsongs, output)
    # output.close()

    # metalsongs, jazzsongs = getData(numTotal)
    # metalsongsTrain = metalsongs[:numTrain]
    # jazzsongsTrain = jazzsongs[:numTrain]
    # popsongsTrain = popsongs[:numTrain]
    # hiphopsongsTrain = hiphopsongs[:numTrain]
    # rocksongsTrain = rocksongs[:numTrain]
    # allSongsTrain = metalsongsTrain + jazzsongsTrain + popsongsTrain + hiphopsongsTrain + rocksongsTrain
    # clusters = KMeans(allSongsTrain, metalsongs, jazzsongs, popsongs, hiphopsongs, rocksongs)
    # metalsongsTest = metalsongs[numTrain:]
    # jazzsongsTest = jazzsongs[numTrain:]
    # popsongsTest = popsongs[numTrain:]
    # hiphopsongsTest = hiphopsongs[numTrain:]
    # rocksongsTest = rocksongs[numTrain:]
    # passedMetal = 0
    # passedJazz = 0
    # passedHipHop = 0
    # passedPop = 0
    # passedRock = 0
    # for song in metalsongsTest:
    #     distance = []
    #     for centroid in clusters:
    #         x = getKLDivergence(song.meanVector, centroid.meanVector, song.covarianceMatrix, centroid.covarianceMatrix)
    #         y = getKLDivergence(centroid.meanVector, song.meanVector, centroid.covarianceMatrix, song.covarianceMatrix)
    #         distance.append(x+y)
    #     val, idx = min((val, idx) for (idx, val) in enumerate(distance))
    #     if(idx == 0):
    #         passedMetal +=1 
    # print passedMetal
            

    # for song in jazzsongsTest:
    #     distance = []
    #     for centroid in clusters:
    #         x = getKLDivergence(song.meanVector, centroid.meanVector, song.covarianceMatrix, centroid.covarianceMatrix)
    #         y = getKLDivergence(centroid.meanVector, song.meanVector, centroid.covarianceMatrix, song.covarianceMatrix)
    #         distance.append(x+y)
    #     val, idx = min((val, idx) for (idx, val) in enumerate(distance))
    #     if(idx == 1):
    #         passedJazz +=1 
    # print passedJazz

    # for song in hiphopsongsTest:
    #     distance = []
    #     for centroid in clusters:
    #         x = getKLDivergence(song.meanVector, centroid.meanVector, song.covarianceMatrix, centroid.covarianceMatrix)
    #         y = getKLDivergence(centroid.meanVector, song.meanVector, centroid.covarianceMatrix, song.covarianceMatrix)
    #         distance.append(x+y)
    #     val, idx = min((val, idx) for (idx, val) in enumerate(distance))
    #     if(idx == 2):
    #         passedHipHop +=1 
    # print passedHipHop

    # for song in popsongsTest:
    #     distance = []
    #     for centroid in clusters:
    #         x = getKLDivergence(song.meanVector, centroid.meanVector, song.covarianceMatrix, centroid.covarianceMatrix)
    #         y = getKLDivergence(centroid.meanVector, song.meanVector, centroid.covarianceMatrix, song.covarianceMatrix)
    #         distance.append(x+y)
    #     val, idx = min((val, idx) for (idx, val) in enumerate(distance))
    #     if(idx == 3):
    #         passedPop +=1 
    # print passedPop

    # for song in rocksongsTest:
    #     distance = []
    #     for centroid in clusters:
    #         x = getKLDivergence(song.meanVector, centroid.meanVector, song.covarianceMatrix, centroid.covarianceMatrix)
    #         y = getKLDivergence(centroid.meanVector, song.meanVector, centroid.covarianceMatrix, song.covarianceMatrix)
    #         distance.append(x+y)
    #     val, idx = min((val, idx) for (idx, val) in enumerate(distance))
    #     if(idx == 4):
    #         passedRock +=1 
    # print passedRock

if __name__ == "__main__" :
    main()


# data = rocksongs[0].featureVectors
# data = data
# # meanVector = getMeanVector(data)
# # covarianceMatrix = getCovarianceMatrix(data, meanVector)
# dataTwo = rocksongs[1].featureVectors
# dataTwo = dataTwo

            

##        tags, genre = getTagsAndGenre(fullname)
##        if genre=='neither':
##            continue
##        if genre=='jazz':
##            jazzfilenames.append(fullname)
##        elif genre=='rock':
##            rockfilenames.append(fullname)
            

##def printp(index):
##    print filenames[index]
##    print tagslist[index]
##    print genrelist[index]
        
        

