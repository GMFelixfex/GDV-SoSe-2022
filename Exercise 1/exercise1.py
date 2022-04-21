import cv2
import math
import operator as op
import numpy as np


# Function for the Circle Path
def circle_path(t, scale, offsetY, offsetX):
    res = (int(scale*math.cos(t)+offsetX), 
           int(scale*math.sin(t)+offsetY))
    return res

# Setting base height and Width
height = 100
width = 256

# Creating empty 256x100 Grayscale image
img = np.zeros((height, width, 1), np.uint8)

# Timer value and incrementing speed
timer = -4.0
timer_increment = -0.01

# Size variable for Video
video_size = ()

# Array for All frames for the Video
img_array = []

# Loop for Displaying the frames
while (True):
    #Creating the Gradient
    for i in range(height):
        for j in range(width):
            img[i][j] = j


    # Resizing do to Lag
    img_alt = cv2.resize(img,(0,0),fx=4,fy=4)
    
    # Getting new Height and Width
    height2 = img_alt.shape[0]
    width2 = img_alt.shape[1]

    # Note to remember: IMG[von-höhe:bis-höhe, von-breite:bis-breite]
    
    # 4x4-Area copied
    small_square = img_alt[height2//2-2:height2//2+2, 
                           width2//2-2:width2//2+2]

    # Scaling the 4x4-area to 50x50                       
    small_square = cv2.resize(small_square, (0,0), fx=12.5, fy=12.5)

    # Getting the circle path
    pt1 = circle_path(timer, 600, -300, width2//2-20)

    # Scaling and Mapping to a 50x50 box
    size = (50, 50)
    pt2 = tuple(map(op.add, pt1, size))

    # Old Code idea
    #imgu = cv2.rectangle(imgu, pt1, pt2, int(gray), cv2.FILLED )

    # Creating the moving Box
    img_alt[pt1[1]:pt2[1], pt1[0]:pt2[0]] = small_square

    # Check if the box should turn around
    if (timer <= -5.6 or timer >= -3.8):
        timer_increment = -timer_increment

    # Timer increamenting
    timer += timer_increment

    # Old Code idea
    #pt1x = (50,50)
    #pt2x = (100,100)
    #pt1x2 = (width2-50,50)
    #pt2x2 = (width2-100,100)
    #imgu = cv2.rectangle(imgu, pt1x, pt2x, int(gray), cv2.FILLED )
    #imgu = cv2.rectangle(imgu, pt1x2, pt2x2, int(gray), cv2.FILLED )

    # Extra Boxes in the Left and Right Corner
    img_alt[50:100, 50:100] = small_square
    img_alt[50:100, width2-100:width2-50] = small_square

    img_array.append(img_alt)
    # Displaying the image
    cv2.imshow('Gradient Illusion', img_alt)

    # Press q to close the window
    if (cv2.waitKey(10) == ord('q')):
        video_size = (img_alt.shape[1],img_alt.shape[0])
        break

# Creating Endscreen
img = np.zeros((400, 1024, 1), np.uint8)
img = cv2.putText(img, 'Press "E" to Export the Video', 
                 (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 
                  1, 127, 2)
img = cv2.putText(img, 'Press "W" to Close the Application', 
                 (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 
                  1, 127, 2)

# Loop for Displaying the Endscreen and Saving the Video
while(True):

    # Shows Endscreen
    cv2.imshow('Gradient Illusion', img)

    # Press e for Video Export
    if (cv2.waitKey(10) == ord('e')):
        # Video Export vie VideoWriter
        fourcc =  cv2.VideoWriter_fourcc(*'DivX')
        out = cv2.VideoWriter('videos/test.mp4', 
                              fourcc, 60.0, 
                              video_size, False)

        # Writing every frame to Video
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        break
    
    # Press w to Close the Application
    if (cv2.waitKey(10) == ord('w')):
        break

# Closing the Application
cv2.destroyAllWindows()


