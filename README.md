# DishDetector
Simple raspberry pi setup to detect dishes in a sink and notify through Slack. 

## Why?
My problem: Two teenage kids who think we've got a maid on staff and “forget” to put their dishes in dishwasher.

## Solution
Initiating a dish investigation when I find dishes in the sink doesn’t work. Providing immediate feedback to correct a behavior does; yet, I don’t have the time to sit by the sink and monitor who’s not doing their job. A pi can. 

The pi has a simple job. Take a pic every x minutes and look for dishes. If dishes are found in the image then upload the image to a slack channel the entire family monitors.  

![notification](https://github.com/ericalexanderorg/DishDetector/blob/master/docs/images/example_detection.jpg?raw=true)

## Development notes
This project had 3 goals: simple, detect dishes, notify

I originally wanted to use OpenCV with some object detection and deep learning to detect any dish in the sink (odd shaped pans, spatulas, etc). It didn’t take long to realize the processing power of a pi-zero can’t handle that load

OpenCV has some great algorithms to detect an image has changed. That seemed like a reasonable option if I couldn’t use ML. Kitchens tend to be busy places and this didn’t work. Too many false positives. 

The final solution uses OpenCV to look for circles in the image. It’s not fallible but seems to strike the right balance between the pi-zero processing power and the goal of detecting dishes. Your results may vary. 

When a dish is found I’m notifying through slack. It doesn’t determine who left the dish there and it can easily be ignored. 

Some features that may be beneficial in the future and should be easy to add:

Trigger dish detection on motion to capture who left the dish there
Shut off the internet for my kids devices if dishes are found

I liked the idea of keeping this self contained in the pi but it would be easy to use any old internet enabled camera that uploads the image to AWS for processing. Drop the image in an S3 bucket, use Rekognition to detect dishes, then alert through SNS or a lambda function. 

The pi-zero is small but it’s still not attractive in the kitchen. It’s very possible my wife will protest soon and I’ll need to work on a hidden camera setup. Then again, she’s already happy the kids are responding. 

