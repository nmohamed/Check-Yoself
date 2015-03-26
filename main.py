"""
Check your posture when lifting.
Software Design 2015
"""
import cv2
import numpy as np

def do_video():
	cap = cv2.VideoCapture(0)
	while(True):
		# Create fram
		ret, frame = cap.read()

		# Display the resulting frame
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# Release the capture
	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	do_video()
####zarin commit