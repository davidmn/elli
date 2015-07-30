# File: import-features.py
# Author: David Megins-Nicholas
# Created: 2015/07/30

import os
import numpy as np

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

# open, load and close the dirty files generated from import-features.py
sittingIn = open(rootPath+"/data/sitting.dat","r")
uprightIn = open(rootPath+"/data/upright.dat","r")

dirtySitting = np.load(sittingIn)
dirtyUpright = np.load(uprightIn)

sittingIn.close()
uprightIn.close()

# clean the files, removing "features" that are 
# just from array initialisation in import-features.py
# then save them to files for processing later
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