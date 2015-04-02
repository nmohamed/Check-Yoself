"""
Functions to compare a video of you doing an exercise to stock photos of you doing an
exercise.
"""


import cv2
import numpy as np

def compare():
	pass

def show_color():
	cap = cv2.VideoCapture(0)
	while(True):
		# Create frame
		ret, frame = cap.read()

		# Convert BGR to HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# define range of blue color in HSV
		lower_blue = np.array([100,200,50])
		upper_blue = np.array([190,255,255])

		# Threshold the HSV image to get only blue colors
		mask = cv2.inRange(hsv, lower_blue, upper_blue)

		# Bitwise-AND mask and original image
		res = cv2.bitwise_and(frame,frame, mask= mask)

		#cv2.imshow('frame',frame)
		#cv2.imshow('mask',mask)
		cv2.imshow('res',res)

		if cv2.waitKey(1) & 0xFF == ord('q'): 
			break

	# Release the capture
	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	show_color()