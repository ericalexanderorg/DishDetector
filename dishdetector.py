import numpy as np
import argparse
import cv2
import copy
import os
from slackclient import SlackClient

#Set our threshold, our circle detecting sensitivity
circle_sensitivity = 40


print("Acquiring Image")
# Note: Larger images require more processing power and have more false positives
os.system("raspistill -w 1024 -h 768 -o /var/www/html/images/process.jpg")
image = cv2.imread("/var/www/html/images/process.jpg")

print("Copying image")
output = copy.copy(image)
print("Blurring image")
blurred = cv2.GaussianBlur(image, (9, 9), 2, 2)
print("Converting to grey")
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

print("Detecting circles in blurred and greyed image")
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, circle_sensitivity) #That last int is our sensitivity, may need tweaking
 
print("Checking if we found images")
if circles is not None:
        print("Dishes Found!")
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
 
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        
        print("Writing detected image") 
        cv2.imwrite('/var/www/html/images/detected.jpg', output)

        print("Sending slack message")
        slack_token = os.environ["SLACK_BOT_TOKEN"]
        sc = SlackClient(slack_token)
        sc.api_call('files.upload', channels=to, filename='Dishes_Detected.jpg', file=open('/var/www/html/images/detected.jpg', 'rb'))

else: 
        print("No Dishes Found!")
