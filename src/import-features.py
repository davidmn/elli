# File: import-features.py
# Author: David Megins-Nicholas

import cv2
import numpy as np 
import os
import glob

# work out where the script is being run for
rootPath = os.path.abspath("..")

# work out the relative paths for the detector to use
modelPath = rootPath+'/PartsBasedDetector/models/Person_8parts.xml'
framePath = rootPath+'/data/currentFrame.png'
detectorPath = rootPath+'/PartsBasedDetector/src/src/PartsBasedDetector'
inFilePath = rootPath+'/src/data.txt'

# upright position is True
# sitting position is False
mode = False

# get the list of target videos depending on the mode
if mode:
	videos = glob.glob(rootPath+"/data/walking/*.avi")
else:
	videos = glob.glob(rootPath+"/data/sitting/*.avi")

# pre allocate the pose array to make life easier and faster
poseArray = np.zeros([9,2,30000])
index = 0

# loop over all videos in the directory
for video in videos:
	print video
	# open the video stream, in this case we use video rather
	# than a webcam stream
	videoStream = cv2.VideoCapture(video)
	while True:
		# sample the video, taking a frame and
		# downsampling for use in the detector
		ret,frame = videoStream.read()
		if frame == None:
			break

		downsampledFrame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25) 
		frameSize = downsampledFrame.shape

		# produce a string that contains the paths to the PBD binary,
		# model file and current frame then run PBD
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

		# convert to numpy array with two columns free for rectangle centres.
		# doing it this way so centres can be calculated in two lines
		pose = np.zeros([len(floatData),6], dtype=float)
		for i in xrange(0,pose.shape[0]):
			for j in xrange(0,pose.shape[1]-2):
				pose[i,j] = floatData[i][j]
			

		# calculate the centers of the rectangles
		pose[:,4] = pose[:,0] + np.divide(pose[:,2], 2)
		pose[:,5] = pose[:,1] + np.divide(pose[:,3], 2)

		# this is the feature vector in image space
		featureVector = np.zeros([9,2])
		featureVector[:,:] = pose[:,4:]

		# normalise the feature vector (feature vector in unit space)
		featureVector[:,0] = np.divide(featureVector[:,0],frameSize[1])
		featureVector[:,1] = np.divide(featureVector[:,1],frameSize[0])

		# put the feature vector in the array
		poseArray[:,:,index] = featureVector
		index = index + 1


if mode:
	outFile = open(rootPath+"/data/upright.dat","w")
else:
	outFile = open(rootPath+"/data/sitting.dat","w")

# the most important step, save the data to a file and exit gracefully
np.save(outFile,poseArray)
outFile.close()

