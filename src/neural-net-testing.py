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

#load neural network
networkFile = open(rootPath+"/networks/network2.pkl",'r')
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
	#false positives
	sittingROC[0,counter] = float(sittingCorrect)/float(len(sittingSet))
	#true positives
	sittingROC[1,counter] = float(sittingIncorrect)/float(len(standingSet))
	counter = counter + 1
	sittingROC[2,counter] = threshold
plt.plot(sittingROC[0,0:100],sittingROC[1,0:100])
plt.show()

