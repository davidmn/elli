# File: neural-net-testing.py
# Author: David Megins-Nicholas

import os
import pybrain as pb
import numpy as np
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import pickle
import matplotlib.pyplot as plt
import glob

rootPath = os.path.abspath("..")

#get list of networks
networks = glob.glob(rootPath+"/networks/*.pkl")

#load test dataset 
testSetFile = open(rootPath+"/data/trainingSet","r")
testSet = pickle.load(testSetFile)
testSetFile.close()
print "dataset loaded"
# initialise lists for sorting roc integration values and accuracy values
areaDetails = []
accDetails = []
for thing in networks:
	print thing[33:-4]
for  networkInstance in networks:
	#load neural network
	networkFile = open(networkInstance,'r')
	print "using network " + str(int(str((networkInstance)[40:-4])))
	network = pickle.load(networkFile)
	networkFile.close()
	print "network loaded"
	
	# activate the network on the data set
	results = []
	for element in testSet:
		results.append([float(network.activate(element[0])),int(element[1])])
	
	# sort data into approriot sets
	sittingSet = []
	standingSet = []
	
	for element in results:
		if element[1] == 0:
			sittingSet.append(element[0])
		if element[1] == 1:
			standingSet.append(element[0])
	
	print np.mean(sittingSet)
	print np.mean(standingSet)
	
	# the threshold for the output of the network
	threshold = 0.0
	
	# these store the data for the roc
	sittingROC = np.zeros([2,1000])
	
	# identify TPs and FPs for ROC plot
	counter = 0
	tempAcc = []
	while threshold < 1.0:
		sittingCorrect = 0
		sittingIncorrect = 0
		standingCorrect = 0
		standingIncorrect = 0
		for element in results:
			#true positive
			if (element[0] < threshold) & (element[1] == 0):
				sittingCorrect = sittingCorrect + 1
			# false positive
			if (element[0] < threshold) & (element[1] == 1):
				sittingIncorrect = sittingIncorrect + 1

		threshold = threshold + 0.001
		#tempAcc.append(1.0-float(sittingCorrect + standingCorrect)/float(len(results)))
		#false positives
		sittingROC[0,counter] = float(sittingCorrect)/float(len(sittingSet))
		#true positives
		sittingROC[1,counter] = float(sittingIncorrect)/float(len(standingSet))

		counter = counter + 1

	# output the details
	#accDetails.append([int(str(networkInstance)[40:-4]), max(tempAcc)])
	sittingFile = open(rootPath+"/data/sittingstandingROC/"+str(networkInstance[40:-4])+"sittingROC.pkl","w")
	pickle.dump(sittingROC,sittingFile)
	areaDetails.append([int(str(networkInstance)[40:-4]),np.trapz(sittingROC[1,0:100])])
	sittingFile.close()

# save the larger loop details
#areaFile = open(rootPath+"/data/area_test.pkl","w")
#pickle.dump(areaDetails,areaFile)
#areaFile.close()
#accFile = open(rootPath+"/data/acc.pkl","w")
#pickle.dump(accDetails,accFile)
#accFile.close()

