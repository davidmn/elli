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

areaDetails = []
networkCounter = 2
accDetails = []
for networkInstance in networks:
	#load neural network
	networkFile = open(networkInstance,'r')
	network = pickle.load(networkFile)
	networkFile.close()
	print "network loaded"
	
	#validate
	results = []
	for element in testSet:
		results.append([float(network.activate(element[0])),int(element[1])])
	
	sittingSet = []
	standingSet = []
	
	for element in results:
		if element[1] == 0:
			sittingSet.append(element[0])
		if element[1] == 1:
			standingSet.append(element[0])
	
	print np.mean(sittingSet)
	print np.mean(standingSet)
	
	threshold = 0.0
	
	sittingROC = np.zeros([3,len(results)])
	standingROC = np.zeros([3,len(results)])
	
	counter = 0
	tempAcc = []
	while threshold < 1.0:
		sittingCorrect = 0
		sittingIncorrect = 0
		standingCorrect = 0
		standingIncorrect = 0
		for element in results:
			#true positive
			if (element[0] > threshold) & (element[1] == 0):
				sittingCorrect = sittingCorrect + 1
			# false positive
			if (element[0] > threshold) & (element[1] == 1):
				sittingIncorrect = sittingIncorrect + 1
			# true positive
			if (element[0] < threshold) & (element[1] == 1):
				standingCorrect = standingCorrect + 1
			# false positive
			if (element[0] < threshold) & (element[1] == 0):
				standingIncorrect = standingIncorrect + 1

	
	
		threshold = threshold + 0.01
		tempAcc.append(1.0-float(sittingCorrect + standingCorrect)/float(len(results)))
		#false positives
		sittingROC[0,counter] = float(sittingCorrect)/float(len(sittingSet))
		#true positives
		sittingROC[1,counter] = float(sittingIncorrect)/float(len(standingSet))
		sittingROC[2,counter] = threshold

		standingROC[0,counter] = float(standingCorrect)/float(len(standingSet))

		sittingROC[1,counter] = float(standingIncorrect)/float(len(sittingSet))

		sittingROC[2,counter] = threshold

		counter = counter + 1
	#plt.plot(sittingROC[0,0:100],sittingROC[1,0:100])
	#plt.show()
	accDetails.append([networkCounter, max(tempAcc)])
	sittingFile = open(rootPath+"/data/"+"sittingROC"+str(networkCounter)+"sittingROC.pkl","w")
	standingFile = open(rootPath+"/data/"+"standingROC"+str(networkCounter)+"standingROC.pkl","w")
	pickle.dump(sittingROC,sittingFile)
	pickle.dump(standingROC,standingFile)
	areaDetails.append([networkInstance,np.trapz(sittingROC[1,0:100]),np.trapz(standingROC[1,0:100])])
	sittingFile.close()
	standingFile.close()
	networkCounter = networkCounter + 1

areaFile = open(rootPath+"/data/area.pkl","w")
pickle.dump(areaDetails,areaFile)
areaFile.close()
accFile = open(rootPath+"/data/acc.pkl","w")
pickle.dump(accDetails,accFile)
accFile.close()

for element in areaDetails:
	print element

for element in accDetails:
	print element