import PicAndBall
import cv2.cv as cv
import math
import sys

try:
    capture = cv.CaptureFromCAM(0)
    cv.NamedWindow('win',cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow('thresh',cv.CV_WINDOW_AUTOSIZE)
except:
    print 'No WebCam Data'
    exit()

center = (0,0)
def setUpStuff(FindMe):
    frame = cv.QueryFrame(capture)
    center = ((int)(frame.height/2),(int)(frame.width/2))
    
    infoList=findImage(frame)
    result = displayImage(infoList,frame)
    return (result, infoList)

def drawCircles(cont,img):
    li = None
    if len(cont) != 0:
        moments = cv.Moments(cont,1)
        moments10 = cv.GetSpatialMoment(moments,1,0)
        moments01 = cv.GetSpatialMoment(moments,0,1)
        area = cv.GetCentralMoment(moments,0,0)
        if area > 0:
            x=(int)(moments10/area)
            y=(int)(moments01/area)
            rad = (int)(math.ceil(math.sqrt(area/3.14)))
            cv.Circle(img,(x,y),rad,(255,255,255,0),1,8,0)
            li = [x,y,img,area]
    return li

##def setUpVariables(infoList,FindMe):
##    if FindMe.area != None:
##        if infoList[0][3] > FindMe.area/2:
##            FindMe.area = infoList[0][3]
##            FindMe.centerOfBall = (infoList[0][0],infoList[0][1])
##        else:
##            print 'false area'
##    else:
##        FindMe.area = infoList[0][3]
##        FindMe.centerOfBall = (infoList[0][0],infoList[0][1])
##    return FindMe

def displayImage(infoList,orig):
    result = False
    if infoList == None:
        print "Control Dot Not Located"
        cv.ShowImage('win',orig)
    else:
        cv.ShowImage('thresh',infoList[1])
        cv.ShowImage('win', infoList[0][2])
        result = True
    return (result)

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
    #cv.InRangeS(img2,cv.Scalar(65,75,58),cv.Scalar(75,59,61),tmp)
    cv.InRangeS(img2,cv.Scalar(90,90,185),cv.Scalar(100,100,200),tmp)

    elmt_shape=cv.CV_SHAPE_RECT
    pos = 6
    element = cv.CreateStructuringElementEx(pos*2+1, pos*2+1, pos, pos, elmt_shape)
    cv.Dilate(tmp,tmp,element,6)

    cv.Split(tmp,h,None,None,None)
    storage = cv.CreateMemStorage()

    scan = cv.FindContours(h,storage)
    xyImage=drawCircles(scan,img)

    if xyImage != None:
            return (xyImage,tmp)
    else:
            return None
        
