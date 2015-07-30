import os
import numpy as np

def cleanUp(inArray):
	outArray = np.zeros(inArray.shape[0:2])
	tempFeature = outArray
	for i in xrange(inArray.shape[2]):
		if inArray[:,:,i].flatten().sum() != 0.0:
			tempFeature = inArray[:,:,i]
			outArray = np.dstack([outArray,tempFeature])
	
	return outArray		

rootPath = os.path.abspath("..")

sittingIn = open(rootPath+"/data/sitting.dat","r")
uprightIn = open(rootPath+"/data/upright.dat","r")

dirtySitting = np.load(sittingIn)
dirtyUpright = np.load(uprightIn)

sittingIn.close()
uprightIn.close()

cleanSitting = cleanUp(dirtySitting)
cleanUpright = cleanUp(dirtyUpright)

sittingOut = open(rootPath+"/data/clean-sitting.dat","w")
uprightOut = open(rootPath+"/data/clean-upright.dat","w")

np.save(sittingOut,cleanSitting)
np.save(uprightOut,cleanUpright)

sittingOut.close()
uprightOut.close()

print "Sitting from " + str(dirtySitting.shape) + " to " + str(cleanSitting.shape)
print "Upright from " + str(dirtyUpright.shape) + " to " + str(cleanUpright.shape)