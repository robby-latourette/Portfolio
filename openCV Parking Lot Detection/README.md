# Parking Lot Detection Using openCV 🚗

## Summary ✍️
What this project seeks to do is provide a cost-effective smart parking system that uses a camera and computer vision to determine whether or not any given parking space in a parking lot is available.

## How it Works 🛠️
First, the program takes a picture and then the user maps out all of the parking spaces within said picture. 
Parking spots are mapped out by clicking on the four corners of the parking spot. 
After 4 clicks, a rectangle is drawn.
When the user is finished, they hit the '=' key to go onto the next step.

After the '=' key is hit, the video feed with the rectangles begins.
Using edge detection, parking spots will turn GREEN when the spot is open, and RED if the spot is taken.
A 2nd window called 'Debug' will also open that shows the edge detected video. 
This can be disabled by commenting out the line that says 'cv2.imshow('Debug',edFrame)'.

For night vision mode, increase apertureSize in the edge_detect() method from 3 to 5. 
