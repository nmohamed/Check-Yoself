"""
Functions to compare a video of you doing an exercise to stock photos of you doing an
exercise.
"""

import cv2
import numpy as np
import math

class Detect():
	def __init__(self):
		cv2.namedWindow('cam', 1)
		self.cap = cv2.VideoCapture(0)
		#Initial marker positions
		self.green = [0,0] #wrist
		self.blue = [0,0] #shoulder
		self.red = [0,0] #elbow

		self.run_video()

		# Release the capture
		self.cap.release()
		cv2.destroyAllWindows()


	def run_video(self):
		def bicep_angle():
			if self.blue == [0,0] or self.red == [0,0]:
				return 0
			else:
				vertical_line = math.sqrt((self.blue[0]-self.red[0])**2 + (self.blue[1]-self.red[1])**2)
				actual_vertical_line = math.sqrt((self.blue[0]-self.blue[0])**2 + (self.blue[1]-self.red[1])**2)
				vertical_angle = math.acos(actual_vertical_line/vertical_line)
				return vertical_angle
		while(True):
			# Create frame
			ret, frame = self.cap.read()
			# Convert BGR to HSV
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			# define orange of color in HSV
			lower_blue = np.array([90,50,200])
			upper_blue = np.array([150,255,255])

			lower_red = np.array([150, 50, 200])
			upper_red = np.array([360, 255, 255])

			lower_green = np.array([60, 150, 200])
			upper_green = np.array([90, 255, 255])

			# Threshold the HSV image to get only blue colors
			mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
			mask_red = cv2.inRange(hsv, lower_red, upper_red)
			mask_green = cv2.inRange(hsv, lower_green, upper_green)

			# Bitwise-AND mask and original image
			res_blue = cv2.bitwise_and(frame,frame, mask = mask_blue) #original in HSV
			color_blur_blue = cv2.medianBlur(res_blue, 5) #blurred color image
			imgray_blue = cv2.cvtColor(color_blur_blue,cv2.COLOR_BGR2GRAY) #blurred b&w

			res_red = cv2.bitwise_and(frame,frame, mask = mask_red) #original in HSV
			color_blur_red = cv2.medianBlur(res_red, 5) #blurred color image
			imgray_red = cv2.cvtColor(color_blur_red,cv2.COLOR_BGR2GRAY) #blurred b&w

			res_green = cv2.bitwise_and(frame,frame, mask = mask_green) #original in HSV
			color_blur_green = cv2.medianBlur(res_green, 5) #blurred color image
			imgray_green = cv2.cvtColor(color_blur_green,cv2.COLOR_BGR2GRAY) #blurred b&w

			
			#Do circles
			circles_b = []
			circles_b = cv2.HoughCircles(imgray_blue, cv2.cv.CV_HOUGH_GRADIENT,1, 20, param1=10, 
										param2=25, minRadius=0, maxRadius=0)

			if circles_b is not None:
				for i in circles_b[0,:]:
					self.blue[0] = i[0]
					self.blue[1] = i[1]
					# draw the center of the circle
					cv2.circle(frame, (i[0],i[1]), 2,(255,0,0),3)

			circles_r = []
			circles_r = cv2.HoughCircles(imgray_red, cv2.cv.CV_HOUGH_GRADIENT,1, 20, param1=10, 
										param2=10, minRadius=0, maxRadius=0)

			if circles_r is not None:
				for i in circles_r[0,:]:
					self.red[0] = i[0]
					self.red[1] = i[1]
					# draw the center of the circle
					cv2.circle(frame, (i[0],i[1]),2,(0,0,255),3)

			circles_g = []
			circles_g = cv2.HoughCircles(imgray_green, cv2.cv.CV_HOUGH_GRADIENT,1, 20, param1=12, 
										param2=15, minRadius=0, maxRadius=0)

			if circles_g is not None:
				for i in circles_g[0,:]:
					self.green[0] = i[0]
					self.green[1] = i[1]
					# draw the center of the circle
					cv2.circle(frame, (i[0],i[1]),2,(0,255,0),3)
			
			cv2.line(frame, (self.blue[0], self.blue[1]), (self.red[0], self.red[1]), (0,0,255)) #red to blue line
			cv2.line(frame, (self.green[0], self.green[1]), (self.red[0], self.red[1]), (0,255,0)) #red to green line

			#angle detection
			a = bicep_angle()*57.29
			print a
			if a > 10:
				overlay = frame.copy()
				cv2.rectangle(overlay, (0,0), (640,500), (0,0,255), thickness = -1)
				opacity = .4
				cv2.addWeighted(overlay, opacity, frame, 1-opacity, 0, frame)
				#cv2.line(frame, (100,100), (400,400), (0,255,255))
			
			#if blue is shoulder, red is elbow, green is hand:\
			cv2.imshow('frame', color_blur_green)


			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				cv2.destroyWindow('cam')
				break

if __name__ == "__main__":
	Detect()