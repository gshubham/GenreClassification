import numpy

'''
Private function for this module, not needed for the user.

Args:
The start index of the window
earlyEndIndex: an endIndex estimate that is <= to the actual endIndex. If you have no estimate pass in startIndex twice.
startTimes, windowLengthSeconds self-explanatory.

Output: returns the actual endIndex to use, exclusive; should go startIndex inclusive to returned Index, but not including returned index.
It returns -1 when there are no more windows.
'''
def getWindowEndIndex(startIndex, earlyEndIndex, startTimes, windowLengthSeconds):
    numSegments = len(startTimes)
    
    windowStartTime = startTimes[startIndex]
    windowEndTime = startTimes[earlyEndIndex]
    while (windowEndTime - windowStartTime) < windowLengthSeconds:
         earlyEndIndex+=1
         if earlyEndIndex >= numSegments:
             return -1
         windowEndTime = startTimes[earlyEndIndex]
    #here the end index has overshot
    return earlyEndIndex

'''
Private function for use in this module only.
Given a list of vectors, return the mean and diagonal
of the covariance matrix.
'''
def calculateGaussianDiagonalCov(vectors):
    means = []

    #calculate the means.
    for featureIndex in range(len(vectors[0])): #for each feature
        total = 0
        for vecIndex in range(len(vectors)): #for each vector
            total+=vectors[vecIndex][featureIndex]
        total/=float(len(vectors))
        means.append(total)

    covs = []
    #calculate the covariances
    for featureIndex in range(len(vectors[0])):
        mean = means[featureIndex]
        total = 0
        for vecIndex in range(len(vectors)):
            error = (mean - vectors[vecIndex][featureIndex])**2
            total+=error
        total/=float(len(vectors))
        covs.append(total)

    return means, covs




'''
Args:
textureSegments are the ones used to calculate the gaussian window.
startTimes are the start times of those texture segments.
windowLengthSeconds is how long (in seconds) you want your window to be.

useConfidences specifies whether to discard windows containing low-confidence estimates.
If true, you must also pass in confidences.

Output: a list of textureWindows.
Each one is a vector of length twice that of a textureSegment. First first n entries are the mean vector,
the last n entries are the diagonals of the covariance matrix.
'''

def calculateTextureWindows(textureSegments, startTimes, windowLengthSeconds, useConfidences=False, confidences = []):
    numSegments = len(textureSegments)
    assert( len(textureSegments)==len(startTimes))
    assert( numSegments > 0), "No segments"

    if useConfidences:
        assert(len(confidences) == len(textureSegments))
        assert False, "Code using confidence values has not been implemented yet."

    textureWindows = []
    
    windowStartIndex = 0
    windowEndIndex = getWindowEndIndex(windowStartIndex, windowStartIndex, startTimes, windowLengthSeconds)
    while( windowEndIndex != -1 ): #when false, you've gone past the end and are done.
        mean, covDiag = calculateGaussianDiagonalCov(textureSegments[windowStartIndex:windowEndIndex]) #end not inclusive.
        textureWindow = mean + covDiag
        textureWindows.append(textureWindow)
        windowStartIndex+=1
        windowEndIndex = getWindowEndIndex(windowStartIndex, windowEndIndex, startTimes, windowLengthSeconds)
        
    return textureWindows
