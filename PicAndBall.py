################################################################
#	Filename: 		PicAndBall.py
#
#	Author: 			Matthew Bachman
#
# Description:  this file creates a datastructure to contain all the information needed by
#							autopilot.py and is meant to be passed from demo2.py to autopilot.py and
#							back again.
#
#	License: 		Feel free to use, distribute, modify, change, destroy, sell, or anything else you
#							could think of doing with this software.  It is distributed with no warrenty and
#							no garuntee that it will work for you.
#
# Tested On:  	Ubuntu 12.0.4 64bit, Python 2.7, AR.Drone2.
#
# Created On: 10/2/2012 
#
#################################################################

import cv2.cv as cv


class PicAndBall:
    def __init__(self,centArea,CAMNUM, c,cOb=None,a=None,center=None):
        self.centerOfBall = cOb
        self.count = c
        self.center = center
        self.area = a
        self.CENTERALAREA = centArea
        self.capture = cv.CaptureFromCAM(0)
        cv.NamedWindow('win',cv.CV_WINDOW_AUTOSIZE)
        cv.NamedWindow('thresh',cv.CV_WINDOW_AUTOSIZE)

    def updateWin(frame):
        cv.ShowImage('win',frame)

    def updateThresh(frame):
        cv.ShowImage('thresh',frame)
 
