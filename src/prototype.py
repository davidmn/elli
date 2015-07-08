import cv2
import numpy as np 
import os


# The paths of the files used in the detection section
videoPath = '/home/megaslippers/elli/data/S2walking3A1.avi'
modelPath = '/home/megaslippers/elli/PartsBasedDetector/models/Person_8parts.xml'
framePath = '/home/megaslippers/elli/data/currentFrame.png'
detectorPath ='/home/megaslippers/elli/PartsBasedDetector/src/src/PartsBasedDetector'
inFilePath = '/home/megaslippers/elli/PartsBasedDetector/src/src/data.txt'

# open the video stream, in this case we use video rather than a webcam stream
videoStream = cv2.VideoCapture(videoPath)

# sample the video, taking a frame and downsampling for use in the detector
ret,frame = videoStream.read()
downsampledFrame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25) 

# produce a string that contains the paths to the PBD binary, model file and current frame then run PBD
cv2.imwrite(framePath,downsampledFrame)
command = detectorPath + ' ' + modelPath + ' ' + framePath
os.system(command)

# open the data file and convert from floats to strings
rawDataString = [line.rstrip('\n') for line in open(inFilePath)]
floatData = []
for element in rawDataString:
	tempData = element.split(',')
	tempFloats = []
	for item in tempData:
		tempFloats.append(float(item))

	floatData.append(tempFloats)


