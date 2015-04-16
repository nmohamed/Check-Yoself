"""
Check your posture when lifting.
Software Design 2015
"""

import cv2
import numpy as np
from Tkinter import *


class MakeWindow(Frame):
	def __init__(self, master):

		# Initialize GUI & frame
		self.master = master
		self.button_frame = Frame(self.master, width = 400, height = 400, colormap = 'new')
		self.button_frame.pack(fill = X)
		self.add_button()

	def add_button(self):
		# Quit Button
		Button(self.button_frame, text = 'Quit', command = quit).pack(fill = X)
		# Pushup Botton
		Button(self.button_frame, text = 'Bicep Curls', command = lambda:self.do_video()).pack(fill=X)

	def do_video(self):
		cap = cv2.VideoCapture(0)
		while(True):
			# Create frame
			ret, frame = cap.read()

			# Display the resulting frame
			cv2.imshow('frame',frame)
			if cv2.waitKey(1) & 0xFF == ord('q'): #currently, press 'q' stops it but doesnt delete the video window
				break
		# Release the capture
		cap.release()
		cv2.destroyAllWindows()


if __name__ == "__main__":
	root = Tk()
	ex = MakeWindow(root)
	root.mainloop() 
