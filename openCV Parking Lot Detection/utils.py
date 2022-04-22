import cv2
import csv
import pandas as pd
import parking_spot as ps

'''
NAME       :    get_parking_list
PARAMETERS :    data         - tuple list of coordinate points
RETURNS    :    parking_list - list of ParkingSpot objects

DESCRIPTION:    -Creates a list of ParkingSpot objects 
                -Populates the 'dimensions' attribute of each object with a list of 2 points 
                based off the information passed in through the parameters
                    -point 1 is the 2nd smallest x and y values from the set of 4 points
                    -point 2 is the 2nd largest  x and y values from the set of 4 points
                -Populates the 'pixels' attribute of each object with the number of pixels 
                within the new rectangle 
'''
def get_parking_list(data):
    #List of ParkingSpot Objects
    parking_list = []

    for i in (range(0,len(data), 4)):

        #Gets the next 4 points from data and sorts the x and y values from low to high
        tempX = [data[i][0],data[i+1][0],data[i+2][0],data[i+3][0]]
        tempY = [data[i][1],data[i+1][1],data[i+2][1],data[i+3][1]]
        tempX.sort()
        tempY.sort()
        
        #Creates new rectangle based on 2nd and 3rd largest x and y values
        newDimensions = [[tempX[1],tempY[1]], [tempX[2],tempY[2]]]

        #Calculates number of pixels inside new rectangle
        pixelsCount = (tempX[2] - tempX[1]) * (tempY[2] - tempY[1])

        #Appends ParkingSpot to the list
        parking_list.append(ps.ParkingSpot(isTaken=False, dimensions=newDimensions, pixels=pixelsCount))
    
    return parking_list


'''
NAME       :    edge_detect
PARAMETERS :    frame   - an image 
RETURNS    :    edFrame - an image after edge detection is applied

DESCRIPTION:    - Grayscaled an image passed into function
                - Blurs the grayscaled image
                    - Blurring reduces noisiness of the image so edge detection works better
                - Applies edge detection to the image
'''
def edge_detect(frame):
    gray      = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)  
    edFrame   = cv2.Canny(image=blur_gray, threshold1=50, threshold2=150, apertureSize=3)
    return edFrame


'''
NAME       :    draw_user_lines
PARAMETERS :    frame        - an image 
                parking_list - list of ParkingSpot objects
RETURNS    :    frame        - an image

DESCRIPTION:    - Determines what color the parking spot boxes should be
                based on ParkingSpot.isTaken
                - Draws parking space boxes on the image
'''
def draw_user_lines(frame, parking_list):
    
    #Colors for Lines
    TAKEN = (0,0,255)
    OPEN  = (0,255,0)

    data = pd.read_csv('COORDS.csv')
    data = data.values.tolist()


    for i in (range(0,len(data), 4)):

        #ParkingSpot.isTaken determines color of lines
        if parking_list[int(i/4)].isTaken:
            color = TAKEN
        else: 
            color = OPEN

        #Draws the user's lines onto the image
        cv2.line(frame, data[i],   data[i+1], color, 1)
        cv2.line(frame, data[i+1], data[i+2], color, 1)
        cv2.line(frame, data[i+2], data[i+3], color, 1)
        cv2.line(frame, data[i+3], data[i],  color, 1)

    return frame

