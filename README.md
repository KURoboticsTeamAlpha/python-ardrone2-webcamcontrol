python-ardrone2-webcamcontrol
=============================
This project takes the code from https://github.com/venthur/python-ardrone 
then adds on top of it.

Taking the Demo program supplied with the code, I added the keyboard command for "autopilot"

autopilot.py is not a true autopilot script.  It reads images from a webcam, then translates the position
of a green plate into a direction of movement.

The openCV code is completely lighting depended, so the HSV values will have to be configured in
findImage() for every lighting condition encountered.

HISTORY:
	10-2-2012 : by Matt Bachman
							-Fixed some syntax errors
							-Added isEmergency variable to libardrone
	10-3-2012: By Matt Bachman
							-Made movement 1 command, allowing diagonal directions.
							
TODO:
	-Add Video Support from the drone
	-Stablize 
