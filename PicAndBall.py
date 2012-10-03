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
 
