import numpy as np
import pandas as pd
import cv2
import csv
import coordinate_mapper as cm
import parking_spot as ps
import utils as ut

#Opens Camera
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    raise Exception("Could not open video device")
cv2.namedWindow('Parking Lot') 

#User maps out coordinates for parking spots
ret, frame = cap.read()
cm.get_coordinates(frame)

#Read in CSV
data = pd.read_csv('COORDS.csv')
data = data.values.tolist()

#Gets List of ParkingSpots
parking_list = ut.get_parking_list(data)

#White Pixel Threshold
wpPercent = .04

#For Debugging Purpose
cv2.namedWindow('Debug')

#Video Loop
while True:
    #Gets new Frame from camera
    ret, frame   = cap.read()

    #Edge Detection
    edFrame = ut.edge_detect(frame)

    for spot in parking_list:
        dimensions   = spot.dimensions
        
        #Crops edge detected image specified by ParkingSpots.dimensions
        tempFrame    = edFrame[dimensions[0][1]:dimensions[1][1], dimensions[0][0]:dimensions[1][0]]

        #Sums all of the white pixels in the frame
        white_pixels = np.sum(tempFrame == 255)

        #Checks if white pixels exceed threshold for a car
        if (white_pixels > (spot.pixels*wpPercent)):
            spot.isTaken = True
        else:
            spot.isTaken = False

    #Draws the lines from the CSV file
    ut.draw_user_lines(frame, parking_list)

    cv2.imshow('Debug',      edFrame)
    cv2.imshow('Parking Lot',frame)

    #Closes program when '=' key is pressed
    if cv2.waitKey(1) == ord('='):
        cv2.destroyAllWindows
        cap.release
        break