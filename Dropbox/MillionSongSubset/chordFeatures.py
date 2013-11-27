

'''
Return true if the first maximum in curr
is also a maximum in next.
We are guaranteed that each of them
has at least one value at 1.0, and that
this is the max value.'''
def isSameDominantFirst(curr, next):
	currDomIndex = -1
	for i in range(len(curr)):
		if curr[i]==1:
			currDomIndex = i
			break

	assert(currDomIndex!=-1), "GUARANTEE BROKEN"
	return next[currDomIndex]==1

'''Given that a note was the loudest in one feature vector,
what is the probability that it is still loudest in the 
next one?'''
def getProbSameDominant(song):
	total = 0
	pitches = song.segments_pitches
	assert(len(pitches)>1), 'Not enough pitches for this song.'
	for i in range(len(pitches)-1):
		curr = pitches[i]
		next = pitches[i+1]
		if isSameDominantFirst(curr, next):
			total+=1
	return total/(len(pitches)-1)


def extractChordFeatures(song):
	features = []
	probStable = getProbSameDominant(song)
	features.append(probStable)
	return features 
