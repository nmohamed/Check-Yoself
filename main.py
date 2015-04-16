"""
Check your posture when lifting.
Software Design 2015
"""
import cv2
import numpy as np
from Tkinter import *
from process_video import *

class MakeWindow(Frame):
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
		Button(self.button_frame, text = 'Bicep Curls', command = lambda:self.do_video()).pack(fill=X)
		Button(self.button_frame, text = 'Pushup').pack(fill = X)
		Button(self.button_frame, text = 'Deadlift').pack(fill = X)
		Button(self.button_frame, text = 'Lunge').pack(fill = X)
		Button(self.button_frame, text = 'Quit', command = quit).pack(fill = X)


	def do_video(self):
		Detect()


if __name__ == "__main__":
	root = Tk()
	ex = MakeWindow(root)
	root.mainloop() 
