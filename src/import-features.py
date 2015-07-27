import cv2
import numpy as np 
import os
import pylab as plt
import pandas as pd
import glob

#sort out paths
rootPath = os.path.abspath("..")
print rootPath

# The paths of the files used in the detection section
videoPath = rootPath+'/data/S2walking3A1.avi'
print videoPath
modelPath = rootPath+'/PartsBasedDetector/models/Person_8parts.xml'
framePath = rootPath+'/data/currentFrame.png'
detectorPath = rootPath+'/PartsBasedDetector/src/src/PartsBasedDetector'
inFilePath = rootPath+'/src/data.txt'

#upright position is True
#sitting position is False
mode = True

#open the relevant pandas panels
if mode:
	exportPanel = pd.read_pickle(rootPath+'/data/upright.pkl')
else:
	exportPanel = pd.read_pickle(rootPath+'/data/sitting.pkl')

# open the video stream, in this case we use video rather than a webcam stream
videoStream = cv2.VideoCapture(videoPath)

#get the list of target videos


while True:
	# sample the video, taking a frame and downsampling for use in the detector
	ret,frame = videoStream.read()
	if frame == None:
		break

	downsampledFrame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25) 
	frameSize = downsampledFrame.shape

	# produce a string that contains the paths to the PBD binary, model file and current frame then run PBD
	cv2.imwrite(framePath,downsampledFrame)
	command = detectorPath + ' ' + modelPath + ' ' + framePath
	os.system(command)

	# open the data file and convert from floats to strings
	rawDataString = [line.rstrip('\n') for line in open(inFilePath)]
	if rawDataString[0] == "break": #checking for null pose
		print "no pose"
		continue

	floatData = []
	for element in rawDataString:
		tempData = element.split(',')
		tempFloats = []
		for item in tempData:
			tempFloats.append(float(item))

		floatData.append(tempFloats)

	# convert to numpy array with two columns free for rectangle centres
	pose = np.zeros([len(floatData),6], dtype=float)
	for i in xrange(0,pose.shape[0]):
		for j in xrange(0,pose.shape[1]-2):
			pose[i,j] = floatData[i][j]
		

	# calculate the centers and split into feature vector
	pose[:,4] = pose[:,0] + np.divide(pose[:,2], 2)
	pose[:,5] = pose[:,1] + np.divide(pose[:,3], 2)
	featureVector = pose[:,4:]

	#normalise the feature vector
	featureVector[:,0] = np.divide(featureVector[:,0],frameSize[1])
	featureVector[:,1] = np.divide(featureVector[:,1],frameSize[0])

	# center the data
	centeredVector = featureVector
	centeredVector[:,0] = centeredVector[:,0] - np.average(centeredVector[:,0])
	centeredVector[:,1] = centeredVector[:,1] - np.average(centeredVector[:,1])

	# show scatter
	plt.scatter(featureVector[:,0],featureVector[:,1])
	plt.axis([-1,1,-1,1])
	#plt.show()

	# create a pandas panel to store data
	temp = np.zeros([9,2,2])
	temp[:,:,0] = featureVector
	temp[:,:,1] = featureVector
	exportPanel = pd.Panel(temp,items=xrange(0,9,1),major_axis=['x','y'],minor_axis=xrange(0,2,1))
	#print p.loc[:,:,0].T
	tempdf = pd.DataFrame(featureVector,index=exportPanel.items, columns=exportPanel.major_axis)
	exportPanel.ix[:,:,2] = tempdf.T
	#print p.loc[:,:,2].T

if mode:
	exportPanel.to_pickle(rootPath+'/data/upright.pkl') 
else:
	exportPanel.to_pickle(rootPath+'/data/sitting.pkl')

