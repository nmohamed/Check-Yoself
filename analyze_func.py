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
		vert_line = distance_formula(marker1, marker2)
		actual_vertical_line = vertical_line(marker1, marker2)
		vertical_angle = math.acos(actual_vertical_line/vert_line)
		return vertical_angle

def straight_body(marker1, marker2, marker3, marker4):
	""" Makes sure your body is straight. marker1 is at top of body, 
		marker2 is at feet"""
	overall = math.acos(horizontal_line(marker1, marker4)/distance_formula(marker1, marker4))
	upper_mid = math.acos(horizontal_line(marker1, marker2)/distance_formula(marker1, marker2))
	lower_mid = math.acos(horizontal_line(marker3, marker4)/distance_formula(marker3, marker4))

	if abs(lower_mid-overall) > 10:
		return False
	elif abs(upper_mid-overall) > 10:
		return False
	else:
		return True

#####

def distance_formula(a, b):
	""" Gets distance between two points """
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def horizontal_line(a, b):
	""" Gets distance of horizontal line, where the beginning of the line is 
		the first point, going up to the x value of the second point"""
	return distance_formula(a, [b[0], a[1]])

def vertical_line(a, b):
	""" Gets distance of vertical line, where the beginning of the line is 
		the first point, going up to the y value of the second point"""
	return distance_formula(a, [a[0], b[1]])