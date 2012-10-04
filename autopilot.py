################################################################
#	Filename: 		autopilot.py
#
#	Author: 			Matthew Bachman
#
# Description:  this file allow the control of the AR.Drone and AR.Drone2 with a webcam
#							and a green plate.  The plate color is green and is completely lighting
#							dependent.  This file is meant to run with of demo2.py and is dependent 
#							on libraries of opencv, math and is also dependent on the files libardrone.py 
#							and PicAndBall.py
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
import math
import libardrone
import PicAndBall


def autopilot(drone,PnB):
        if PnB.count == 0:
                frame = cv.QueryFrame(PnB.capture)
	PnB.count += 1
	frame = cv.QueryFrame(PnB.capture)
	if PnB.center[0] == 0 and PnB.center[1] == 0:
                PnB.center = ((int)(frame.height/2),(int)(frame.width/2))
        infoList=findImage(frame)
        results = displayImage(infoList,frame, PnB)
        PnB = results[1]
        if results[0]:
                PnB = setUpVariables(infoList, PnB)
                return (setMovementControls(drone, PnB),PnB)
        return (drone,PnB)

#infoList contains ((x,y,img,area),thresholded image)
def displayImage(infoList,orig, PnB):
    result = False
    if infoList == None:
        print "Control Dot Not Located"
        PnB.updateWin(orig)
    else:
        PnB.updateThresh(infoList[1])
        PnB.updateWin(infoList[0][2])
        result = True
    return (result,PnB)

def setUpVariables(infoList,PnB):
    if PnB.count >= 1 and PnB.area != None:
        if infoList[0][3] > PnB.area/2:
            PnB.area = infoList[0][3]
            PnB.centerOfBall = (infoList[0][0],infoList[0][1])
        else:
            print 'false area'
    elif PnB.count == 1 or PnB.area == None:
        PnB.area = infoList[0][3]
        PnB.centerOfBall = (infoList[0][0],infoList[0][1])
    return PnB

def setMovementControls(drone,PnB):
    amtH = 0
    amtV = 0
    amtT= 0
    amtY =0
    if (PnB.centerOfBall == None or PnB.area == None) or ((PnB.centerOfBall[0]>=PnB.center[0]-5 and PnB.centerOfBall[0]<=PnB.center[0]+5)
                                                  and(PnB.centerOfBall[1]>=PnB.center[1]-5 and PnB.centerOfBall[1]<=PnB.center[1]+5)
                                                  and (PnB.area >= PnB.CENTERALAREA - 10 and PnB.area <= PnB.CENTERALAREA + 10)):
        drone.hover()
        print 'hovering'
    else:
        #horizontal controls
        if PnB.centerOfBall[0] < PnB.center[0]-5:
        	amtH=testPercent(PnB.centerOfBall[0],PnB.center[0])
        	print 'moving right at ' + amtH +' amount of speed'
            #drone.speed = (testPercent(PnB.centerOfBall[0],PnB.center[0]))
            #drone.move_left()
        elif PnB.centerOfBall[0] > PnB.center[0]+5:
        	amtH=-testPercent((PnB.center[0]*2)-PnB.centerOfBall[0],PnB.center[0])
        	print 'moving right at '+ amtH +' amount of speed'
            #drone.speed = testPercent((PnB.center[0]*2)-PnB.centerOfBall[0],PnB.center[0])
            #drone.move_right()
            
        #vertical controls
        if PnB.centerOfBall[1] < PnB.center[1]-5:
        	amtV = -testPercent(PnB.centerOfBall[1],PnB.center[1])
        	print 'moving down at ' + amtV +' amount of speed'
		if PnB.centerOfBall[1] > PnB.center[1]+5:
			amtV = testPercent((PnB.center[1]*2)-PnB.centerOfBall[1],PnB.center[1])
			print 'moving up at '+ amtV +' amount of speed'
            #drone.speed = testPercent((PnB.center[1]*2)-PnB.centerOfBall[1],PnB.center[1])
            #drone.move_up()
            

        #front back controls
        if PnB.area < PnB.CENTERALAREA - 10:
        	amtY = -testPercent(PnB.area,PnB.CENTERALAREA)
        	print 'moving front at '+ amtY+' amount of speed'
            #drone.speed = testPercent(PnB.area,PnB.CENTERALAREA)
            #drone.move_front()
            
        elif PnB.area > PnB.CENTERALAREA + 10:
        	amtY = testPercent((PnB.CENTERALAREA*2)-PnB.area,PnB.CENTERALAREA)
        	print 'moving back at '+ amtY +' amount of speed'
            #drone.speed = testPercent((PnB.CENTERALAREA*2)-PnB.area,PnB.CENTERALAREA)
            #drone.move_back()
            
		drone.at(at_pcmd, True,amtH, amtY,amtV, 0)
    return drone

def testPercent(numberTo, test):
    if numberTo>=(test):
        return 1.0
    elif numberTo>=(test*.9):
        return .9
    elif numberTo>=(test*.8):
        return .8
    elif numberTo>=(test*.7):
        return .7
    elif numberTo>=(test*.6):
        return .6
    elif numberTo>=(test*.5):
        return .5
    elif numberTo>=(test*.4):
        return .4
    elif numberTo>=(test*.3):
        return .3
    elif numberTo>=(test*.2):
        return .2
    elif numberTo>=(test*.1):
        return .1
    return 0

def drawCircles(cont,img):
    li = None
    if len(cont) != 0:
        moments = cv.Moments(cont,1)
        moments10 = cv.GetSpatialMoment(moments,1,0)
        moments01 = cv.GetSpatialMoment(moments,0,1)
        area = cv.GetCentralMoment(moments,0,0)
        if area > 0:
            x=(int)(moment10/PnB.area)
            y=(int)(moment01/PnB.area)
            rad = (int)(math.ceil(math.sqrt(PnB.area/3.14)))
            cv.Circle(img,(x,y),rad,(255,255,255,0),1,8,0)
            li = [x,y,img,area]
    return li

def findImage(img):
    #Set up storage for images
    frame_size = cv.GetSize(img)
    img2 = cv.CreateImage(frame_size,8,3)
    tmp = cv.CreateImage(frame_size,8,cv.CV_8U)
    h = cv.CreateImage(frame_size,8,1)

    #copy original image to do work on
    cv.Copy(img,img2)

    #altering the image a bit for smoother processing
    cv.Smooth(img2,img2,cv.CV_BLUR,3)
    cv.CvtColor(img2,img2,cv.CV_BGR2HSV)

    #make sure temp is empty
    cv.Zero(tmp)

    #detection based on HSV value
    #30,100,90 lower limit on pic 41,255,255 on pic
    #cv.InRangeS(img2,cv.Scalar(25,100,87),cv.Scalar(50,255,255),tmp)
    #Range for green plate dot in my Living room
    #cv.InRangeS(img2,cv.Scalar(55,80,60),cv.Scalar(65,95,90),tmp)
    #classroom
    #cv.InRangeS(img2,cv.Scalar(55,80,60),cv.Scalar(70,110,70),tmp)
    #Kutztowns Gym
    cv.InRangeS(img2,cv.Scalar(65,100,112),cv.Scalar(85,107,143),tmp)

    elmt_shape=cv.CV_SHAPE_ELLIPSE
    pos = 3
    element = cv.CreateStructuringElementEx(pos*2+1, pos*2+1, pos, pos, elmt_shape)
    cv.Dilate(tmp,tmp,element,6)
    cv.Erode(tmp,tmp,element,2)

    cv.Split(tmp,h,None,None,None)
    storage = cv.CreateMemStorage()

    scan = sc.FindContours(h,storage)
    xyImage=drawCircles(scan,img)

    if xyImage != None:
            return (xyImage,tmp)
    else:
            return None
        
