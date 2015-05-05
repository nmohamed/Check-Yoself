class Camera():
	""" OpenCV stuff"""
	def __init__(self, exercise):
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
		self.do_exercise(exercise)

	def do_exercise(self, exercise):
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
				self.draw_bicep(red.marker_pos, blue.marker_pos) #input exercise

			elif exercise == 'Lunge':
				# find positions of markers
				blue.get_marker(self.hsv, self.frame)
				orange.get_marker(self.hsv, self.frame)

				#based on marker position, analyse
				self.draw_lunge(orange.marker_pos, blue.marker_pos) #input exercise      

			elif exercise == 'Pushup' or exercise == 'Plank':
				# find positions of markers
				blue.get_marker(self.hsv, self.frame)
				red.get_marker(self.hsv, self.frame)
				green.get_marker(self.hsv, self.frame)
				orange.get_marker(self.hsv, self.frame)

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
		""" blue: marker position of blue marker, same with red
			draw_blue/draw_red = last seen position of markers for drawing persistent line"""
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
		#blue-knee toe-orangle
		self.draw_blue = self.draw_circles(blue_pos, (255,0,0), self.draw_blue)
		self.draw_orange = self.draw_circles(orange_pos, (0,0,255), self.draw_orange)

		cv2.rectangle(self.frame,(self.draw_orange[0],self.draw_orange[1]),(2*self.draw_orange[0]-self.draw_blue[0],2000),(0,0,255))

		pos_status = af.knee_toe(self.draw_orange, self.draw_blue)

		if pos_status == True:
			self.show_error()

	def draw_pushup(self, blue_pos,orange_pos,red_pos,green_pos):
		""" blue: marker position of blue marker, same with red
			draw_blue/draw_red = last seen position of markers for drawing persistent line"""
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
		if self.timer > 5:
			self.timer = 0
		if self.timer == 0:
			pygame.init()
			pygame.mixer.music.load("buzzer_x.wav")
			pygame.mixer.music.play()
			self.timer = time.sleep(.01)

		
# Controller
class Detect():
	""" Finds marker based on color input and can output position of marker"""
	def __init__(self, low, up):
		#Initial marker positions
		self.marker_pos = [0, 0]
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
						20, param1=10, param2=5, minRadius=0, maxRadius=0)
		
		self.marker_pos = circles