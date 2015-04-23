"""
Check your posture when lifting.
Software Design 2015
"""
import cv2
import numpy as np
import math
from Tkinter import *
import analyze_func as af

# The view
class MakeWindow(Frame):
	""" Does ugly GUI stuff"""
	def __init__(self, master):
		# Initialize GUI & frame
		self.master = master
		self.button_frame = Frame(self.master, width = 400, height = 400, colormap = 'new')
		self.button_frame.pack(fill = X)
		self.add_button()

	def add_button(self):
		#Button(self.button_frame, text = 'Tutorial').pack(fill = X)
		#Button(self.button_frame, text = 'Check Yourself').pack(fill = X)
		# Pushup Botton
		Button(self.button_frame, text = 'Bicep Curls', command = lambda:Camera('Bicep Curl')).pack(fill=X)
		Button(self.button_frame, text = 'Pushup').pack(fill = X)
		Button(self.button_frame, text = 'Deadlift').pack(fill = X)
		Button(self.button_frame, text = 'Lunge').pack(fill = X)
		Button(self.button_frame, text = 'Quit', command = quit).pack(fill = X)

# The second view
class Camera():
	""" OpenCV stuff"""
	def __init__(self, exercise):
		self.cap = cv2.VideoCapture(0)
		if exercise == 'Bicep Curl':
			blue = Detect([70,50,150], [150,255,255])
			blue.marker_pos = [0, 0]
			red = Detect([150, 50, 150] , [360, 255, 255])
			red.marker_pos = [0,0]
			self.draw_blue = [0,0]
			self.draw_red = [0,0]
		#green = Detect([30, 150, 100,  70, 255, 255])

		while(True):
			# Create frame
			self.ret, self.frame = self.cap.read()
			# Convert BGR to HSV
			self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

			#get the markers
			if exercise == 'Bicep Curl':
				# find positions of markers
				blue.get_marker(self.hsv, self.frame)
				red.get_marker(self.hsv, self.frame)

				#based on marker position, analyse
				self.draw_bicep(blue.marker_pos, red.marker_pos) #input exercise
				print self.draw_blue
			
			# Show frame
			cv2.imshow('frame', self.frame)

			# Exit frame
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# Release the capture
		self.cap.release()
		cv2.destroyAllWindows()

	def draw_bicep(self, blue, red):
		""" blue: marker position of blue marker, same with red
			draw_blue/draw_red = last seen position of markers for drawing persistent line"""
		#draw circles
		self.draw_blue = self.draw_circles(blue, (255,0,0), self.draw_blue)
		self.draw_red = self.draw_circles(red, (0,0,255), self.draw_red)

		#draw limbs
		cv2.line(self.frame, (self.draw_blue[0], self.draw_blue[1]), (self.draw_red[0], self.draw_red[1]), (0,0,255)) #red to blue line

		#find angle
		bicep_angle = af.straight_upperarm(self.draw_blue, self.draw_red)

		#tell you if you're wrong
		a = bicep_angle*57.29 #CONVERT FROM RADIANS

		if a > 10:
			self.show_error()

	def draw_circles(self, circles, color, last_found):
		""" Draws a circle where the marker is detected and also returns the position of the first marker"""
		if circles is not None:
			for i in circles[0,:]:
				last_found[0] = i[0]
				last_found[1] = i[1]
				cv2.circle(self.frame, (i[0],i[1]), 2, color,3)
		return last_found

	def show_error(self):
		"""  Shows that you're doing the exercise wrong. Currently makes the window red"""
		overlay = self.frame.copy()
		cv2.rectangle(overlay, (0,0), (640,500), (0,0,255), thickness = -1)
		opacity = .4
		cv2.addWeighted(overlay, opacity, self.frame, 1-opacity, 0, self.frame)
		
# Controller
class Detect():
	""" Finds marker based on color input and can output position of marker"""
	def __init__(self, low, up):
		#Initial marker positions
		self.marker_pos = []

		self.low = low
		self.up = up

	def get_marker(self, hsv, frame):
		"""gets marker location"""
		# Threshold the HSV image to get only one color
		lower = np.array(self.low)
		upper = np.array(self.up)
		mask = cv2.inRange(hsv, lower, upper)

		res = cv2.bitwise_and(frame,frame, mask = mask) #original in HSV
		color_blur = cv2.medianBlur(res, 5) #blurred color image
		imgray = cv2.cvtColor(color_blur,cv2.COLOR_BGR2GRAY) #blurred b&w

		# Find color cricles
		circles = []
		circles = cv2.HoughCircles(imgray, cv2.cv.CV_HOUGH_GRADIENT,1,
		 				20, param1=10, param2=25, minRadius=0, maxRadius=0)
		
		self.marker_pos = circles

if __name__ == "__main__":
	root = Tk()
	ex = MakeWindow(root)
	root.mainloop() 