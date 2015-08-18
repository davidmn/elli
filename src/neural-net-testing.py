import os
import pybrain as pb
import numpy as np
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import pickle

rootPath = os.path.abspath("..")

#load test dataset 
testSetFile = open(rootPath+"/data/testSet","r")
testSet = pickle.load(testSetFile)
testSetFile.close()
print "dataset loaded"

#load neural network
networkFile = open(rootPath+"/networks/network17.pkl",'r')
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