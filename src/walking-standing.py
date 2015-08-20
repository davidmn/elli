import numpy as np 
import os
import matplotlib.pyplot as plt
import pickle 

def cleanUp(inArray):
	""" takes 3D numpy array, iterates along the 3rd axis removing features
	(2D slices) that are empty (left over after feature importing), returns
	a 3D numpy array """
	outArray = np.zeros(inArray.shape[0:2])
	tempFeature = outArray
	for i in xrange(inArray.shape[2]):
		if inArray[:,:,i].flatten().sum() != 0.0:
			tempFeature = inArray[:,:,i]
			outArray = np.dstack([outArray,tempFeature])
	
	return outArray[:,:,1:]	

rootPath = os.path.abspath("..")

standingIn = open(rootPath+"/data/standing.dat","r")
walkingIn = open(rootPath+"/data/walking.dat","r")

standingDirty = np.load(standingIn)
walkingDirty = np.load(walkingIn)

standingClean = cleanUp(standingDirty)
walkingClean = cleanUp(walkingDirty)

print "from " + str(standingDirty.shape) + " to " + str(standingClean.shape)
print "from " + str(walkingDirty.shape) + " to " + str(walkingClean.shape)
standingrocAreas = []
walkingrocAreas = []
timesampledAcc = []

for timeSample in xrange(1,100,10):
	threshold = 0.0
	standingROC = np.zeros([2,100000])
	walkingROC = standingROC
	rocCounter = 0
	x = []
	y = []
	x2 = []
	y2 = []
	acc = []
	while threshold < 1.0:
		standingTruePositives = 0
		standingFalsePositives = 0
		walkingTruePositives = 0
		walkingFalsePositives = 0
		standingDiffs = []
		for i in xrange(timeSample,standingClean.shape[2]-1):
			previousPosition = standingClean[:,:,i-timeSample]
			currentPosition = standingClean[:,:,i]
			xPrev = np.average(previousPosition[:,0])
			yPrev = np.average(previousPosition[:,1])
			xCur = np.average(currentPosition[:,0])
			yCur = np.average(currentPosition[:,1])
			xDiff = xCur - xPrev
			yDiff = yCur - yPrev
			mag = np.sqrt((xDiff*xDiff)+(yDiff*yDiff))
			standingDiffs.append(mag)
		
		walkingDiffs = []
		for i in xrange(99,walkingClean.shape[2]-1):
			previousPosition = walkingClean[:,:,i-100]
			currentPosition = walkingClean[:,:,i]
			xPrev = np.average(previousPosition[:,0])
			yPrev = np.average(previousPosition[:,1])
			xCur = np.average(currentPosition[:,0])
			yCur = np.average(currentPosition[:,1])
			xDiff = xCur - xPrev
			yDiff = yCur - yPrev
			mag = np.sqrt((xDiff*xDiff)+(yDiff*yDiff))
			walkingDiffs.append(mag)
	
		for mag in standingDiffs:
			if mag < threshold:
				standingTruePositives = standingTruePositives + 1
			if mag > threshold:
				walkingFalsePositives = walkingFalsePositives + 1
	
		for mag in walkingDiffs:
			if mag > threshold:
				walkingTruePositives = walkingTruePositives + 1
			if mag < threshold:
				standingFalsePositives = standingFalsePositives + 1
	
		standingTP = float(standingTruePositives)/float(len(standingDiffs))
		standingFP = float(standingFalsePositives)/float(len(walkingDiffs))
		walkingTP = float(walkingTruePositives)/float(len(walkingDiffs))
		walkingFP = float(walkingFalsePositives)/float(len(standingDiffs))
		x.append(standingFP)
		y.append(standingTP)
		x2.append(walkingFP)
		y2.append(standingTP)
		threshold = threshold + 0.01
		rocCounter = rocCounter + 1
		acc.append(float(standingTruePositives+walkingTruePositives)/float(len(walkingDiffs)+len(standingDiffs)))
	
	standingexportRoc = np.zeros([2,len(x)])
	standingexportRoc[0,:] = np.array(x)
	standingexportRoc[1,:] = np.array(y)
	standingexportFile = open(rootPath+"/data/standingwalkingROC/"+"standingsamplerate"+str(timeSample)+".pkl","w")
	pickle.dump(standingexportRoc,standingexportFile)
	standingexportFile.close()

	walkingexportRoc = np.zeros([2,len(x2)])
	walkingexportRoc[0,:] = np.array(x2)
	walkingexportRoc[1,:] = np.array(y2)
	walkingexportFile = open(rootPath+"/data/standingwalkingROC"+"walkingsamplerate"+str(timeSample)+".pkl",'w')
	pickle.dump(walkingexportRoc,walkingexportFile)
	walkingexportFile.close()

	standingrocAreas.append(np.trapz(y))
	walkingrocAreas.append(np.trapz(y2))
	timesampledAcc.append(max(acc))



standingexportArea = open(rootPath+"/data/standingwalkingROC/standingareas.pkl","w")
walkingexportArea = open(rootPath+"/data/standingwalkingROC/walkingAreas.pkl","w")
pickle.dump(standingrocAreas,standingexportArea)
pickle.dump(walkingrocAreas,walkingexportArea)
standingexportArea.close()
walkingexportArea.close()

accExport = open(rootPath+"/data/standingwalkingROC/acc.pkl","w")
pickle.dump(timesampledAcc,accExport)
accExport.close()

x = xrange(1,100,10)
plt.plot(x,standingrocAreas)
plt.plot(x,walkingrocAreas)
plt.show()