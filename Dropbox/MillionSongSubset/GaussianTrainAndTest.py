import os
import h5py

class Song:
    def __init__(self, fname):
        f = h5py.File(fname, 'r')
        self.fname = fname
        self.tags = self.getTags(f)
        self.genre = self.getGenre(self.tags)
        if self.genre=='neither':
            return
        self.featureVectors, self.confidences = self.getFeatureVectorsAndConf(f)
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
            if conf<.6:
                continue
            item = mfcc2d[i]
            confValues.append(conf)
            featureVectors.append(item)
            
        return featureVectors, confValues
   
    def getTags(self, f):
        tags = f['metadata']['artist_terms']
        alltags = []
        for tag in tags:
            alltags.append(tag)
        return alltags

    def getGenre(self, tags):
        top5 = tags[:5]
        numjazz = 0
        numrock = 0
        for tag in top5:
            if 'rock' in tag:
                numrock+=1
            if 'jazz' in tag:
                numjazz+=1

        if numrock>=1 and numjazz==0:
            return 'rock'
        if numjazz>=1 and numrock==0:
            return 'jazz'
        return 'neither'

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


##def pp(index):
##    print 'jazz'
##    l = []
##    for genresong in jazzsongs[:30]:
##        l.append(genresong.avgMFCC[index])
##    l.sort()
##    print l
##
##    l = []
##    print '\nrock'
##    for genresong in rocksongs[:30]:
##        l.append(genresong.avgMFCC[index])
##    l.sort()
##    print l
	    
def fillSongs(numNeeded):
    rocksongs = []
    jazzsongs = []

    total=0
    songdir = "data/A"
    for subdir in os.listdir(songdir):
        name = songdir + "/"+subdir
        
        for ssubdir in os.listdir(name):
            name2 = name+"/"+ssubdir
            print name2
            
            for fname in os.listdir(name2):
                fpath = name2+"/"+fname
                print fpath
                print min(len(rocksongs), len(jazzsongs))
                if len(rocksongs)>=numNeeded and len(jazzsongs)>=numNeeded:
                    return rocksongs[:numNeeded], jazzsongs[:numNeeded]
                currsong = Song(fpath)
                if currsong.genre == 'jazz':
                    jazzsongs.append(currsong)
                elif currsong.genre=='rock':
                    rocksongs.append(currsong)
                else:
                    assert(currsong.genre=='neither')
    return rocksongs[:numNeeded], jazzsongs[:numNeeded]

def getData(numPerGenre):
    rocksongs, jazzsongs = fillSongs(numPerGenre)
    assert( len(rocksongs)==numPerGenre and len(jazzsongs)==numPerGenre) #if false then need more data
    return rocksongs, jazzsongs


