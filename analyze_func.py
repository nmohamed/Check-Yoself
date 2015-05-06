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
		vert_line = dis(marker1, marker2)
		actual_vertical_line = vertical_line(marker1, marker2)
		vertical_angle = math.acos(actual_vertical_line/vert_line)
		return vertical_angle

def straight_body(p1, p2, p3, p4):
	""" Makes sure your body is straight. marker1 is at top of body, 
		marker4 is at feet"""
	if p1 == [0,0] or p2 == [0,0] or p3 == [0,0] or p4 == [0,0]:
		return 0
	else:
		if abs(check_angle(p1,p2,p3)-180)>10 or abs(check_angle(p1,p2,p4)-180)>10 or abs(check_angle(p1,p3,p4)-180)>10 or abs(check_angle(p2,p3,p4)-180)>10:
			return True
		else:
			return False


def knee_toe(marker1,marker2):
	""" Find whether one's knee passes his toes when doing lunge."""
	if marker1 == [0,0] or marker2 == [0,0]:
		return 0

	else:
		if marker1[0]-marker2[0]>=0:
			return True
		else:
			return False

#####
def check_angle(p1,p2,p3):
	# p2 is the vertex
	ang= math.degrees(math.acos((dis(p1,p2)**2+dis(p2,p3)**2-dis(p1,p3)**2)/(2*dis(p1,p2)*dis(p2,p3))))
	return ang

def dis(p1, p2):
	""" Gets distance between two points """
	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def horizontal_line(a, b):
	""" Gets distance of horizontal line, where the beginning of the line is 
		the first point, going up to the x value of the second point"""
	return dis(a, [b[0], a[1]])

def vertical_line(a, b):
	""" Gets distance of vertical line, where the beginning of the line is 
		the first point, going up to the y value of the second point"""
	return dis(a, [a[0], b[1]])