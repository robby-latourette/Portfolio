import cv2
import csv

from cv2 import destroyAllWindows

#Global Variables
coordinates = [] #Stores all points that the user selects
clicks = 0       #Counter to keep track of how many times the user clicks m1
recCount = 0     #Counter for the total amount of rectangles drawn

'''
NAME       :    get_coordinates
GLOBALS    :    coordinates - List of tuples holding x,y coordinates determined by user
                clicks      - Counter that keeps track of how many times user hit Mouse 1
                                - Potential values are 0-4
                recCount    - Keeps track of how many rectangles the user has created
PARAMETERS :    frame - an image
RETURNS    :    None

DESCRIPTION:    - Allows the user to map out parking spots by clicking on an image
                    - After 4 clicks, a box is drawn on the image
                - Image closes when user hits the '=' key
'''
def get_coordinates(frame):
      
    '''
    NAME       :    _mouse_callback
    GLOBALS    :    coordinates - List of tuples holding x,y coordinates determined by user
                    clicks      - Counter that keeps track of how many times user hit Mouse 1
                                    - Potential values are 0-4
                    recCount    - Keeps track of how many rectangles the user has created
    PARAMETERS :    event - Holds what key the user pressed
                    x     - X position of click 
                    y     - Y position of click
                    flags,param - I don't know what these do but I need them 
    RETURNS    :    None

    DESCRIPTION:    - When the user presses the Mouse 1 key (LBUTTONDOWN),
                        - The x and y values are appended as a tuple to the list of coordinates
                        - The click counter is incremented by 1
                    - If the click counter is greater than 3
                        - The draw_rectangle function is called
    '''
    def _mouse_callback(event,x,y,flags,param):
        global coordinates,clicks,recCount

        if event == cv2.EVENT_LBUTTONDOWN:
            
            coordinates.append((x,y))
            clicks += 1
        
        if clicks > 3:
            draw_rectangle()
    
    '''
    NAME       :    draw_rectangle
    GLOBALS    :    coordinates - List of tuples holding x,y coordinates determined by user
                    clicks      - Counter that keeps track of how many times user hit Mouse 1
                                    - Potential values are 0-4
                    recCount    - Keeps track of how many rectangles the user has created
    PARAMETERS :    None
    RETURNS    :    None

    DESCRIPTION:    - Draw a rectangle onto an image using user-selected points
                    - After the Rectangle is drawn:
                        - The rectangle counter is incremented by 1
                        - The clicks counter is reset from 4 to 0
    '''
    def draw_rectangle():
        global coordinates, clicks, recCount

        cv2.line(frame, coordinates[(recCount*4)],  coordinates[(recCount*4)+1],(0,255,0), 1)
        cv2.line(frame, coordinates[(recCount*4)+1], coordinates[(recCount*4)+2],(0,255,0), 1)
        cv2.line(frame, coordinates[(recCount*4)+2], coordinates[(recCount*4)+3],(0,255,0), 1)
        cv2.line(frame, coordinates[(recCount*4)+3], coordinates[(recCount*4)],(0,255,0), 1)
        
        recCount += 1
        clicks = 0

    cv2.namedWindow('Parking Lot') 
    cv2.setMouseCallback('Parking Lot',_mouse_callback)



    while True:

        cv2.imshow('Parking Lot', frame)
        #when user is done drawing, = is pressed to escape the loop
        if cv2.waitKey(1) == ord('='):
            write_csv(coordinates)
            break

'''
NAME       :    write_csv
PARAMETERS :    Coordinates - list of points the user selected
RETURNS    :    None

DESCRIPTION:    - Writes user selected points to CSV file
'''
def write_csv(coordinates):
    with open("COORDS.csv", "w") as f:
        writer = csv.writer(f)
        headers = ['x','y']
        writer.writerow(headers)
        for i in coordinates:
            writer.writerow(i)
