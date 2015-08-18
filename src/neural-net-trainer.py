import os
import pybrain as pb
import numpy as np
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import pickle

def buildNetwork(inputs,hidden,outputs):
	""" returns a feed forward neural network using the pybrain library """
	# initialise the network
	network = pb.structure.FeedForwardNetwork()

	# create the layers for the network 
	inLayer = pb.structure.LinearLayer(inputs)
	hiddenLayer = pb.structure.SigmoidLayer(hidden)
	outLayer = pb.structure.LinearLayer(outputs)

	# add layers to the network
	network.addInputModule(inLayer)
	network.addModule(hiddenLayer)
	network.addOutputModule(outLayer)

	# connect the layers
	in2hidden = pb.structure.FullConnection(inLayer, hiddenLayer)
	hidden2out = pb.structure.FullConnection(hiddenLayer, outLayer)

	# add the connections to the network
	network.addConnection(in2hidden)
	network.addConnection(hidden2out)

	# initialise the weights
	network.sortModules()

	return network

def loadData(path):
	""" load data from a numpy array file and return a numpy array """
	f = open(path,"r")
	array = np.load(f)
	f.close()
	return array

def centrePose(array):
	array[:,0,:] = array[:,0,:] - np.average(array[:,0,:])
	array[:,1,:] = array[:,1,:] - np.average(array[:,1,:])
	return array

rootPath = os.path.abspath("..")

sittingData = loadData(rootPath+"/data/clean-sitting.dat")
uprightData = loadData(rootPath+"/data/clean-upright.dat")

# center the data around the origin to make poses in different locations look the same
sittingData = centrePose(sittingData)
uprightData = centrePose(uprightData)

dataSet = SupervisedDataSet(18,1)

# 0 target is sitting
# 1 target is upright
for i in xrange(sittingData.shape[2]):
	dataSet.addSample((sittingData[:,:,i].flatten()),(0,))
for i in xrange(uprightData.shape[2]):
	dataSet.addSample((uprightData[:,:,i].flatten()),(1,))

testSet, trainingSet = dataSet.splitWithProportion(0.25)
testSet.saveToFile(rootPath+"/data/testSet")
trainingSet.saveToFile(rootPath+"/data/trainingSet")


for i in xrange(2,19):
	print "training network with " + str(i) + " neurons"
	network = buildNetwork(18,i,1)
	trainer = BackpropTrainer(network,dataset=trainingSet, momentum=0.1, verbose=True, weightdecay=0.01)
	trainer.trainEpochs(40)

	# save the network
	networkOutFile = open(rootPath+"/networks/network"+str(i)+".pkl","w")
	pickle.dump(network, networkOutFile)
	networkOutFile.close()

print "done"