import cv2
import numpy as np 

def show_image(img):
    cv2.imshow('title',img)
    cv2.waitKey(0) #don't close the window straight away
    cv2.destroyAllWindows() #close all the cv2 windows on exit

img = cv2.imread("obama.jpg",1)

show_image(img)