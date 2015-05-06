"""
Check your posture when lifting.
Software Design 2015
"""
import cv2
import cv
import numpy as np
import math
import Tkinter as tk
import analyze_func as af
import pygame
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# The view
class BaseFrame(tk.Frame):
	""" An abstract base class for the frames that sit inside PythonGUI.
		Args:
			master (tk.Frame): The parent widget.
			controller (PythonGUI): The controlling Tk object.
		Attributes:
			controller (PythonGUI): The controlling Tk object."""

	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		self.controller = controller
		self.grid()
		self.create_widgets()


	def create_widgets(self):
		"""Create the widgets for the frame."""
		raise NotImplementedError


class HomeFrame(BaseFrame):
	"""The application home page.
		Attributes:
			new_button (tk.Button): The button to switch to ExecuteFrame."""

	def create_widgets(self):
		"""Create the base widgets for the frame."""
		self.tutorial = tk.Button(self,anchor=tk.W,command=lambda: self.controller.show_frame(TutorialFrame),padx=5,pady=5,text="Tutorial")
		self.checkyourself = tk.Button(self,anchor=tk.W,command=lambda: self.controller.show_frame(ExerciseFrame),padx=5,pady=5,text="Check Yourself")
		self.help = tk.Button(self, anchor = tk.W, command = lambda: self.controller.show_frame(HelpFrame),padx=5, pady =5, text = "Help")
		self.quit = tk.Button(self,anchor=tk.W,command=quit,padx=5,pady=5,text="Quit")
		self.tutorial.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.checkyourself.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.help.grid(padx=5, pady=5, sticky = tk.W+tk.E)
		self.quit.grid(padx=5, pady=5, sticky=tk.W+tk.E)


class TutorialFrame(BaseFrame):
	"""The application home page.

	Attributes:
	  new_button (tk.Button): The button to switch to HomeFrame.
	"""

	def create_widgets(self):
		"""Create the base widgets for the frame."""
		self.BicepCurls = tk.Button(self,anchor=tk.W,command=lambda: self.showtutorial('biceps.mp4'), padx=5,pady=5,text="Bicep Curls")
		self.Pushup = tk.Button(self,anchor=tk.W,command=lambda: self.showtutorial('pushup.mp4'),padx=5,pady=5,text="Pushup")
		self.Plank = tk.Button(self,anchor=tk.W,command=lambda:self.showtutorial('lunges.mp4'),padx=5,pady=5,text="Plank")
		self.Lunge = tk.Button(self,anchor=tk.W,command=lambda: self.showtutorial('plank.mp4'),padx=5,pady=5,text="Lunge")
		self.back = tk.Button(self,anchor=tk.W,command=lambda: self.controller.show_frame(HomeFrame),padx=5,pady=5,text="Back")
		self.help = tk.Button(self, anchor = tk.W, command = lambda:self.controller.show_frame(HelpFrame), padx=5, pady=5, text="Help" )
		self.quit = tk.Button(self,anchor=tk.W,command=quit,padx=5,pady=5,text="Quit")

		self.BicepCurls.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.Pushup.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.Plank.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.Lunge.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.back.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.help.grid(padx=5, pady=5, sticky = tk.W+tk.E)
		self.quit.grid(padx=5, pady=5, sticky=tk.W+tk.E)


	def showtutorial(self, filename):
		""" Shows a video of how to properly do an exercise. 
				filename: name of video file """

		vidFile = cv.CaptureFromFile(filename)
		nFrames = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_COUNT))
		fps = cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FPS)
		waitPerFrameInMillisec = int(1/fps * 1000/1)

		for f in xrange(nFrames):
			frameImg = cv.QueryFrame(vidFile)
			cv.ShowImage( "Tutorial",  frameImg )
			cv.WaitKey(waitPerFrameInMillisec) 
		cv.DestroyAllWindows(nFrames)

	
class HelpFrame(BaseFrame):
	""" The application help page."""

	def create_widgets(self):
		"""Create base widgets for the frame"""

		self.bicepcurls = tk.Button(self, anchor=tk.W,command=lambda: self.showexercise('bicep.jpg'), padx=5,pady=5,text="Bicep Curls")
		self.pushup = tk.Button(self, anchor=tk.W,command=lambda: self.showexercise('pushup.jpg'), padx=5,pady=5,text="Pushup")
		self.lunge = tk.Button(self, anchor=tk.W,command=lambda: self.showexercise('lunge.jpg'), padx=5,pady=5,text="Lunge")
		self.plank = tk.Button(self, anchor=tk.W,command=lambda: self.showexercise('plank.jpg'), padx=5,pady=5,text="Plank")
		self.back = tk.Button(self,anchor=tk.W,command=lambda: self.controller.show_frame(HomeFrame),padx=5,pady=5,text="Back")
		self.quit = tk.Button(self,anchor=tk.W,command=quit,padx=5,pady=5,text="Quit")

		self.bicepcurls.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.pushup.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.lunge.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.plank.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.back.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.quit.grid(padx=5, pady=5, sticky=tk.W+tk.E)


	def showexercise(self, exercise):
		""" Shows instructions for how to do exercises"""
		image = mpimg.imread(exercise)
		plt.imshow(image)
		plt.show()


class ExerciseFrame(BaseFrame):
	"""The application home page.

	Attributes:
	  new_button (tk.Button): The button to switch to HomeFrame.

	"""

	def create_widgets(self):
		"""Create the base widgets for the frame."""
		self.BicepCurls = tk.Button(self,anchor=tk.W,command=lambda: Camera('Bicep Curl'),padx=5,pady=5,text="Bicep Curls")
		self.Pushup = tk.Button(self,anchor=tk.W,command=lambda: Camera('Pushup'),padx=5,pady=5,text="Pushup")
		self.Plank = tk.Button(self,anchor=tk.W,command=lambda: Camera('Plank'),padx=5,pady=5,text="Plank")
		self.Lunge = tk.Button(self,anchor=tk.W,command=lambda: Camera('Lunge'),padx=5,pady=5,text="Lunge")
		self.back = tk.Button(self,anchor=tk.W,command=lambda: self.controller.show_frame(HomeFrame),padx=5,pady=5,text="Back")
		self.quit = tk.Button(self,anchor=tk.W,command=quit,padx=5,pady=5,text="Quit")

		self.BicepCurls.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.Pushup.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.Plank.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.Lunge.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.back.grid(padx=5, pady=5, sticky=tk.W+tk.E)
		self.quit.grid(padx=5, pady=5, sticky=tk.W+tk.E)


class PythonGUI(tk.Tk):
	"""The main window of the GUI.

	Attributes:
	  container (tk.Frame): The frame container for the sub-frames.
	  frames (dict of tk.Frame): The available sub-frames.
	"""

	def __init__(self):
		tk.Tk.__init__(self)
		self.title("Python GUI")
		self.create_widgets()
		self.resizable(0, 0)


	def create_widgets(self):
		"""Create the widgets for the frame."""             
		#   Frame Container
		self.container = tk.Frame(self)
		self.container.grid(row=0, column=0, sticky=tk.W+tk.E)

		#   Frames
		self.frames = {}
		for f in (HomeFrame, TutorialFrame, ExerciseFrame, HelpFrame): # defined subclasses of BaseFrame
			frame = f(self.container, self)
			frame.grid(row=2, column=2, sticky=tk.NW+tk.SE)
			self.frames[f] = frame
		self.show_frame(HomeFrame)


	def show_frame(self, cls):
		"""Show the specified frame.

		Args:
		  cls (tk.Frame): The class of the frame to show. 

		"""
		self.frames[cls].tkraise()


# The second 'view'
class Camera():
	""" OpenCV stuff"""

	def __init__(self, exercise):
		""" Initialize the markers and showing video"""
		self.cap = cv2.VideoCapture(0)
		self.timer = 0
		self.blue_values = ([92, 150, 200], [150, 255, 255])
		self.red_values = ([150, 150, 150] , [360, 255, 255])
		self.orange_values = ([10, 150, 200], [30, 255, 255])
		self.green_values = ([60, 150, 200], [90, 255, 255])
		self.draw_blue = [0,0]
		self.draw_red = [0,0]
		self.draw_green = [0,0]
		self.draw_orange= [0,0]
		###################################
		# If you have a hard time getting markers to be recognized, play around with these values.
		self.blue_p1 = 10
		self.blue_p2 = 10
		self.red_p1 = 10
		self.red_p2 = 10
		self.green_p1 = 10
		self.green_p2 = 10
		self.orange_p1 = 10
		self.orange_p2 = 10
		###################################
		self.do_exercise(exercise)


	def do_exercise(self, exercise):
		""" This function shows the webcam feed of the user exercising and lets them know
			about their posture. Depending on the exercises, certain markers will be tracked 
			and their positions will be updated."""

		if exercise == 'Bicep Curl':
			blue = Detect(self.blue_values[0], self.blue_values[1])
			red = Detect(self.red_values[0], self.red_values[1])

		elif exercise == 'Lunge':
			blue = Detect(self.blue_values[0], self.blue_values[1])
			orange = Detect(self.orange_values[0], self.orange_values[1])

		elif exercise == 'Pushup' or exercise == 'Plank':
			blue = Detect(self.blue_values[0], self.blue_values[1])
			red = Detect(self.red_values[0], self.red_values[1])
			green = Detect(self.green_values[0], self.green_values[1])
			orange = Detect(self.orange_values[0], self.orange_values[1])

		""" Get images from your webcam and display them."""
		while(True):
			# Create frame
			self.ret, self.frame = self.cap.read()
			# Convert BGR to HSV
			self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

			# Get the markers
			if exercise == 'Bicep Curl':
				# find positions of markers
				blue.get_marker(self.hsv, self.frame, self.blue_p1, self.blue_p2)
				red.get_marker(self.hsv, self.frame, self.red_p1, self.red_p2)

				#based on marker position, analyse
				self.draw_bicep(red.marker_pos, blue.marker_pos) #input exercise

			elif exercise == 'Lunge':
				# find positions of markers
				blue.get_marker(self.hsv, self.frame, self.blue_p1, self.blue_p2)
				orange.get_marker(self.hsv, self.frame, self.orange_p1, self.orange_p2)

				#based on marker position, analyse
				self.draw_lunge(orange.marker_pos, blue.marker_pos) #input exercise      

			elif exercise == 'Pushup' or exercise == 'Plank':
				# find positions of markers
				blue.get_marker(self.hsv, self.frame, self.blue_p1, self.blue_p2)
				red.get_marker(self.hsv, self.frame, self.red_p1, self.red_p2)
				green.get_marker(self.hsv, self.frame, self.green_p1, self.green_p2)
				orange.get_marker(self.hsv, self.frame, self.orange_p1, self.orange_p2)

				#based on marker position, analyse
				self.draw_pushup(red.marker_pos, blue.marker_pos, green.marker_pos, orange.marker_pos) #input exercise

			# Show frame
			cv2.imshow('frame', self.frame)

			# Exit frame
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# Release the capture
		self.cap.release()
		cv2.destroyAllWindows()


	def draw_bicep(self, red_pos, blue_pos):
		""" Evaluates bicep exercise
				blue_pos, red_pos: marker position of blue marker, same with red"""
		#draw circles
		self.draw_blue = self.draw_circles(blue_pos, (255,0,0), self.draw_blue)
		self.draw_red = self.draw_circles(red_pos, (0,0,255), self.draw_red)

		#draw limbs
		cv2.line(self.frame, (self.draw_blue[0], self.draw_blue[1]), (self.draw_red[0], self.draw_red[1]), (0,0,255)) #red to blue line

		#find angle
		bicep_angle = af.straight_upperarm(self.draw_blue, self.draw_red)

		#tell you if you're wrong
		a = bicep_angle*57.29 #CONVERT FROM RADIANS

		if a > 10:
			self.show_error()


	def draw_lunge(self, orange_pos, blue_pos):
		""" Evaluates lunge exercise
				orange_pos, blue_pos: marker positions"""

		#blue-knee toe-orangle
		self.draw_blue = self.draw_circles(blue_pos, (255,0,0), self.draw_blue)
		self.draw_orange = self.draw_circles(orange_pos, (0,0,255), self.draw_orange)

		cv2.rectangle(self.frame,(self.draw_orange[0],self.draw_orange[1]),(2*self.draw_orange[0]-self.draw_blue[0],2000),(0,0,255))

		pos_status = af.knee_toe(self.draw_orange, self.draw_blue)

		if pos_status == True:
			self.show_error()


	def draw_pushup(self, blue_pos,orange_pos,red_pos,green_pos):
		""" Evaluates pushup AND plank exercise
				orange_pos, blue_pos, red_pos, green_pos: marker positions"""

		#shouder-blue,hip-orange,knee-red,ankle-green    
		#draw circles
		self.draw_blue = self.draw_circles(blue_pos, (255,0,0), self.draw_blue)
		self.draw_red = self.draw_circles(red_pos, (0,0,255), self.draw_red)
		self.draw_orange = self.draw_circles(orange_pos, (255,155,0), self.draw_orange)
		self.draw_green = self.draw_circles(green_pos, (0,0,255), self.draw_green)

		#draw limbs
		cv2.line(self.frame, (self.draw_blue[0], self.draw_blue[1]), (self.draw_orange[0], self.draw_orange[1]), (0,0,255)) #red to blue line
		cv2.line(self.frame, (self.draw_orange[0], self.draw_orange[1]), (self.draw_red[0], self.draw_red[1]), (0,0,255))
		cv2.line(self.frame, (self.draw_red[0], self.draw_red[1]), (self.draw_green[0], self.draw_green[1]), (0,0,255))

		pos_status = af.straight_body(self.draw_blue,self.draw_orange,self.draw_red,self.draw_green)
		if pos_status == True:
			self.show_error()


	def draw_circles(self, circles, color, last_seen):
		""" Draws a circle where the marker is detected and also returns the position of the first marker"""
		if circles is not None:
			average = [0, 0]
			count = 0;
			for i in circles[0,:]:
				cv2.circle(self.frame, (i[0],i[1]), 2, color,3)
				average[0] += i[0]
				average[1] += i[1]
				count += 1
			average[0] = int(round(average[0]/count))
			average[1] = int(round(average[1]/count))
			return average
		else:
			return last_seen


	def show_error(self):
		"""  Shows that you're doing the exercise wrong. Currently makes the window red"""
		overlay = self.frame.copy()
		cv2.rectangle(overlay, (0,0), (640,500), (0,0,255), thickness = -1)
		opacity = .4
		cv2.addWeighted(overlay, opacity, self.frame, 1-opacity, 0, self.frame)
		if self.timer > 2.9:
			self.timer = 0
		if self.timer == 0:
			pygame.init()
			pygame.mixer.music.load("buzzer_x.wav")
			pygame.mixer.music.play()
			self.timer = time.sleep(3)

		
# Controller
class Detect():
	""" Finds marker based on color input and can output position of marker"""

	def __init__(self, low, up):
		""" Initial marker positions
				up: higher color threshold
				low: lower color threshold"""
		self.marker_pos = [0, 0]
		self.low = low
		self.up = up


	def get_marker(self, hsv, frame, p1, p2):
		""" Finds marker location """

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
						20, param1=p1, param2=p2, minRadius=0, maxRadius=0)
		
		self.marker_pos = circles


if __name__ == "__main__":
	app = PythonGUI()
	app.mainloop()
	exit()