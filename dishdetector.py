import numpy as np
import argparse
import cv2
import copy
import os
import time
from slackclient import SlackClient
from gpiozero import Buzzer

## Define our config values

# What is our min dish count to alarm on?
min_dishes = 2

# Define areas we want to ignore
# First value is the x range, second is the y range
ignore_list = ["339-345,257-260"]

# Set the GPIO our buzzer is connected to
buzzer = Buzzer(21)

# Set how long we want to buzz
buzz_seconds = 180

# Set our timestamp
time_stamp = time.strftime("%Y%m%d%H%M%S")

# Set our circle detection variables
circle_sensitivity = 40 # Larger numbers increase false positives
min_rad = 30  # Tweak this if you're detecting circles that are too small
max_rad = 75 # Tweak if you're detecting circles that are too big (Ie: round sinks)


# Cropping the image allows us to only process areas of the image
# that should have images. Set our crop values
crop_left = 0
crop_right = 360
crop_top = 150
crop_bottom = 850


def should_ignore(ignore_list, x, y):
	# Loop through our ignore_list and check for this x/y
	ignore = False
	for range in ignore_list:
			x_range = range.split(',')[0]
			y_range = range.split(',')[1]
			x_min = int(x_range.split('-')[0])
			x_max = int(x_range.split('-')[1])
			y_min = int(y_range.split('-')[0])
			y_max = int(y_range.split('-')[1])

			if (x >= x_min and x <= x_max and y >= y_min and y <= y_max):
					ignore = True

	return ignore


def main():

	print("Acquiring Image")
	# Note: Larger images require more processing power and have more false positives
	os.system("raspistill -w 1024 -h 768 -o /var/www/html/images/process.jpg")
	image_original = cv2.imread("/var/www/html/images/process.jpg")
	print("Cropping image to limit processing to just the sink")
	image = image_original[crop_left:crop_right, crop_top:crop_bottom]


	print("Copying image")
	output = copy.copy(image)

	print("Blurring image")
	blurred = cv2.GaussianBlur(image, (9, 9), 2, 2)
	cv2.imwrite('/var/www/html/images/blurred.jpg', blurred)

	print("Converting to grey")
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	cv2.imwrite('/var/www/html/images/gray.jpg', gray)


	print("Detecting circles in blurred and greyed image")
	circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 20,
		      param1=100,
		      param2=circle_sensitivity,
		      minRadius=min_rad,
		      maxRadius=max_rad)

	 
	print("Checking if we found images")
	if circles is not None:
		dish_count = 0
		print("Dishes Found!")
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
	 
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			print("Tracing circle x:%s, y:%s, r:%s" % (x,y,r))
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			# Check our ignore_list
			if (should_ignore(ignore_list, x, y)):	
				print("Circle in ignore_list: Ignoring")
			else: 
				dish_count += 1
				print("Dish count:%s" % (str(dish_count)))
		
		print("Writing detected image") 
		cv2.imwrite('/var/www/html/images/detected.jpg', output)

		if dish_count >= min_dishes:
			print("Starting Buzzer")
			timeout_start = time.time()
			while time.time() < timeout_start + buzz_seconds:
				buzzer.on()
				time.sleep(2)
				buzzer.off()
				time.sleep(1)

	else: 
		print("No Dishes Found!")


if __name__ == "__main__":
    main()
