#!/usr/bin/env python

# Copyright (c) 2011 Bastian Venthur
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Demo app for the AR.Drone.

This simple application allows to control the drone and see the drone's video
stream.
"""


import pygame

import libardrone
import cv2.cv as cv
import math
import sys
import SuS
import PicAndBall



def main():
    pygame.init()
    W, H = 320, 240
    FindMe = PicAndBall.PicAndBall(300,0,0)
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    clock = pygame.time.Clock()
    flying = False
    running = True
    autopylot = False
    #INFO FOR AUTOPILOT WITH OPENCV
    #myInfo = PicAndBall.PicAndBall(300,0,0)
    while running:
        drone.speed = 0.1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYUP:
		if not autopylot:
                    drone.hover()
            elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_o:
		    if autopylot:
			autopylot = False
		    autopylot = True
                elif event.key == pygame.K_ESCAPE:
                    drone.reset()
		    flying = False
                    running = False
                # takeoff / land
                elif event.key == pygame.K_RETURN:
		    drone.takeoff()
                elif event.key == pygame.K_SPACE:
                    drone.land()
                # emergency
                elif event.key == pygame.K_BACKSPACE:
                    drone.reset()
                # forward / backward
                elif event.key == pygame.K_w:
                    drone.move_forward()
                elif event.key == pygame.K_s:
                    drone.move_backward()
                # left / right
                elif event.key == pygame.K_a:
                    drone.move_left()
                elif event.key == pygame.K_d:
                    drone.move_right()
                # up / down
                elif event.key == pygame.K_UP:
                    drone.move_up()
                elif event.key == pygame.K_DOWN:
                    drone.move_down()
                # turn left / turn right
                elif event.key == pygame.K_LEFT:
                    drone.turn_left()
                elif event.key == pygame.K_RIGHT:
                    drone.turn_right()
		
                # speed
                elif event.key == pygame.K_1:
                    drone.speed = 0.1
                elif event.key == pygame.K_2:
                    drone.speed = 0.2
                elif event.key == pygame.K_3:
                    drone.speed = 0.3
                elif event.key == pygame.K_4:
                    drone.speed = 0.4
                elif event.key == pygame.K_5:
                    drone.speed = 0.5
                elif event.key == pygame.K_6:
                    drone.speed = 0.6
                elif event.key == pygame.K_7:
                    drone.speed = 0.7
                elif event.key == pygame.K_8:
                    drone.speed = 0.8
                elif event.key == pygame.K_9:
                    drone.speed = 0.9
                elif event.key == pygame.K_0:
                    drone.speed = 1.0
	if autopylot:
##            try:
##                capture = cv.CaptureFromCAM(0)
##                cv.NamedWindow('win',cv.CV_WINDOW_AUTOSIZE)
##                cv.NamedWindow('thresh',cv.CV_WINDOW_AUTOSIZE)
##            except:
##                print 'No WebCam Data'
##                exit()
            #justMoved[1]=horizontal, justMoved[2] =verticle
            XjustMoved = False
            YneedsMove = False
            ZneedsMove = False
	    while True:
                #PnB.count += 1
##                frame = cv.QueryFrame(capture)
##                if not frame:
##                    frame = cv.QueryFrame(capture)

                #Check to see if a center has been created, if not, create it
                #er[0] == 0 and PnB.center[1] == 0:
                #    PnB.center = ((int)(frame.height/2),(int)(frame.width/2))
                #find the image and display in the frame
                #infoList=findImage(frame)
                #results = displayImage(infoList,frame, PnB)
                
                results = SuS.setUpStuff(FindMe)
                #FindMe = results[0]
                infoList = results[1] 
                #if the dot was located move the drone, else make the drone hover
                if results[0]:
                    FindMe = setUpVariables(infoList,FindMe)
                    if (FindMe.centerOfBall == None or FindMe.area == None) or testCentered(FindMe):
                        drone.hover()
                        print 'hovering'
                    else:
                        #horizontal controls
                        if not XjustMoved and not YneedsMove and not ZneedsMove:
                            if FindMe.centerOfBall[0] < FindMe.center[0]-5:
                                #drone.speed=testPercent(PnB.centerOfBall[0],PnB.center[0])
                                drone.move_right()
                                print 'moving right at '
                                cv.WaitKey(20)
                                XjustMoved = True
                                
                            elif FindMe.centerOfBall[0] > FindMe.center[0]+5:
                                #drone.speed=testPercent((PnB.center[0]*2)-PnB.centerOfBall[0],PnB.center[0])
                                drone.move_left()
                                cv.WaitKey(20)
                                print 'moving left at '
                                XjustMoved = True
            
                            
                        #vertical controls
                        if not YneedsMove:
                            if FindMe.centerOfBall[1] < FindMe.center[1] or FindMe.centerOfBall[1] > FindMe.center[1]:
                                YneedsMove = True
                        else:
                            if FindMe.centerOfBall[1] < FindMe.center[1]:
                                #drone.speed = testPercent(PnB.centerOfBall[1],PnB.center[1])
                                drone.speed = .1
                                drone.move_down()
                                print 'moving down at '
                                cv.WaitKey(20)
                            elif FindMe.centerOfBall[1] > FindMe.center[1]:
                                drone.speed = .1
                                drone.move_up()
                                cv.WaitKey(20)
                                print 'moving up at '
                            YneedsMove = False
                            XjustMoved = False
                                
                                
                            
                        drone.speed = .1
                        #front back controls
                        #if PnB.area < PnB.CENTERALAREA - 50:
                        if not ZneedsMove:
                            if FindMe.are <15000 or FindMe.area > 17000
                        if FindMe.area < 15000:
                            #amtY = -testPercent(PnB.area,PnB.CENTERALAREA)
                            #drone.speed = .3
                            drone.move_forward()
                            cv.WaitKey(20)
                            print 'moving front at '
                            #+ str(amtY)+' amount of speed'
                            #drone.speed = testPercent(PnB.area,PnB.CENTERALAREA)
                            #drone.move_front()
                        #elif PnB.area > PnB.CENTERALAREA + 50:
                        elif FindMe.area > 17000:
                            #amtY = testPercent((PnB.CENTERALAREA*2)-PnB.area,PnB.CENTERALAREA)
                            #drone.speed = .3
                            drone.move_backward()
                            cv.WaitKey(20)
                            print 'moving back at '
                            #+ str(amtY) +' amount of speed'
                            #drone.speed = testPercent((PnB.CENTERALAREA*2)-PnB.area,PnB.CENTERALAREA)
                            #drone.move_back()drone = (setMovementControls(PnB),PnB)
                else:
                    drone.hover()
                if cv.WaitKey(100) == 27:
                    autopylot = False
                    break


        try:
            surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
            # battery status
            hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
            bat = drone.navdata.get(0, dict()).get('battery', 0)
            f = pygame.font.Font(None, 20)
            hud = f.render('Battery: %i%%' % bat, True, hud_color)
            screen.blit(surface, (0, 0))
            screen.blit(hud, (10, 10))
        except:
            pass

        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print "Shutting down...",
    drone.halt()
    print "Ok."





def testCentered(PnB):
    if PnB.centerOfBall[0]>=PnB.center[0]-5 and PnB.centerOfBall[0]<=PnB.center[0]+5:
        if PnB.centerOfBall[1]>=PnB.center[1]-5 and PnB.centerOfBall[1]<=PnB.center[1]+5:
            if PnB.area >= 17000 and PnB.area <= 15000:
                return True
    return False

def setUpVariables(infoList,FindMe):
    if FindMe.area != None:
        if infoList[0][3] > FindMe.area/2:
            FindMe.area = infoList[0][3]
            FindMe.centerOfBall = (infoList[0][0],infoList[0][1])
        else:
            print 'false area'
    else:
        FindMe.area = infoList[0][3]
        FindMe.centerOfBall = (infoList[0][0],infoList[0][1])
    return FindMe


if __name__ == '__main__':
    main()

