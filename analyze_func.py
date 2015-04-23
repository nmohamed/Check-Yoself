"""
Functions to compare a video of you doing an 
exercise to proper form for doing exercise
"""

import math

# Model
def straight_upperarm(marker1, marker2):
	""" Finds angle of how off a limb is from the y-axis
			input: the position of two markers
			output: the angle of how far off the markers are from the y-axis"""
	# print marker1, marker2
	if marker1 == [0,0] or marker2 == [0,0]:
		return 0
	else:
		vertical_line = math.sqrt((marker1[0]-marker2[0])**2 + (marker1[1]-marker2[1])**2)
		actual_vertical_line = math.sqrt((marker1[0]-marker1[0])**2 + (marker1[1]-marker2[1])**2)
		vertical_angle = math.acos(actual_vertical_line/vertical_line)
		return vertical_angle