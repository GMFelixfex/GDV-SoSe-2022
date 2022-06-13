import os
from GDV_TrainingSet import Descriptor, TrainingSet
import cv2
import numpy as np

# Best Match Function from Origonal File
def findBestMatch(trainData, sample):
    # do the matching with FLANN
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(trainData.trainData, sample, k=1)

    # Sort by their distance.
    matches = sorted(matches, key=lambda x: x[0].distance)
    bestMatch = matches[0][0]
    return bestMatch.queryIdx


click_x = 0
click_y = 0
endApp = False
# Click Function, to Select an Image to display
def click(event, x, y, flags, param):
    global click_x
    global click_y

    if event == cv2.EVENT_LBUTTONDOWN:
        click_x = int(round(x,0)/16)
        click_y = int(round(y,0)/16)


# Setting up the Training Data
file_name = 'Exercise 4/data/data'
root_path = 'Exercise 4/data/101_ObjectCategories/'

trainData = TrainingSet(root_path)

# Loading the Image for the Selction Prozess
imgForMosaic =  cv2.imread('Exercise 4/bilder/cat2.png', cv2.IMREAD_COLOR)
imgForMosaic =  cv2.resize(imgForMosaic,(1024,1024))

# Displaying the Original Iamge for the key input
cv2.namedWindow("Original Image",cv2.WINDOW_AUTOSIZE)
cv2.imshow("Original Image",imgForMosaic)

discriptors = [Descriptor.TINY_COLOR4,Descriptor.TINY_COLOR8,Descriptor.TINY_COLOR16,Descriptor.TINY_COLOR_PIXEL,Descriptor.TINY_GRAY4,Descriptor.TINY_GRAY8]
selectedDiscriptor = 0
gotSelected = False

print("Select Discriptor with W and S, and confirm with D")
print(str(discriptors[selectedDiscriptor]))

# Code for the Discriptor Selection
while not gotSelected:
    key = cv2.waitKey(0) & 0xFF

    # Quitting
    if (key == ord("q")):
        endApp = True
        break

    # Selection and Selection Printing
    elif (key == ord("w") or (key == ord("s"))):
        if (key == ord("w")):
            selectedDiscriptor = selectedDiscriptor+1
        else:
            selectedDiscriptor = selectedDiscriptor-1

        if selectedDiscriptor >= len(discriptors):
            selectedDiscriptor = 0
        elif selectedDiscriptor < 0:
            selectedDiscriptor = len(discriptors) - 1
        print("Selected discriptor: "+str(discriptors[selectedDiscriptor]))
    
    # Confirmation of Discriptor
    elif (key == ord("d")):
        gotSelected = True
        file_name = file_name + str(discriptors[selectedDiscriptor])+".npz"






if not endApp:
    if os.path.isfile(file_name):
        # Decide if you want to Train or Load the Data
        print("If you want to load the training data press R otherwise press any other key")
        key = cv2.waitKey(0) & 0xFF
        if (key == ord("r")):
            trainData.loadTrainingData(file_name)
        else:
            trainData.createTrainingData(discriptors[selectedDiscriptor])
            trainData.saveTrainingData(file_name)
    else:
        print("No training data found, will beginn training...")
        trainData.createTrainingData(discriptors[selectedDiscriptor])
        trainData.saveTrainingData(file_name)


    # Dividing the Image in 4096 tiles
    imgArray = []
    for i in range(64):
        for k in range(64):
            imgArray.append(imgForMosaic[i*16:i*16+16,k*16:k*16+16])

    bestMatchedImages = []
    bestMatchedImagesFull = []
    bestMatchedImagesPart=[]

    # assuring that the same descriptor is used by reading it from the training data set
    assert(isinstance(trainData.descriptor, Descriptor))
    descr = trainData.descriptor

    # Matching a tile to a Picture
    for i in range(len(imgArray)):
        newcomer = np.ndarray(shape=(1, descr.getSize()),
                        buffer=np.float32(descr.compute(imgArray[i])),
                        dtype=np.float32)
        idx = findBestMatch(trainData, newcomer)

        # Reading hte Picture
        matchedImage = cv2.imread(trainData.getFilenameFromIndex(idx), cv2.IMREAD_COLOR)

        # Resizing and addihng the picture to 2 lists
        bestMatchedImages.append(cv2.resize(matchedImage,(16,16)))
        bestMatchedImagesPart.append(matchedImage)
        if(i%64 == 0 and i > 0):
            # Creating a 2d List
            bestMatchedImagesFull.append(bestMatchedImagesPart)
            bestMatchedImagesPart = []
        
        key = cv2.waitKey(1) & 0xFF

        # Quitting mid image generation
        if (key == ord("q")):
            endApp = True
            break
            
        print("Picture Tile: "+str(i+1)+" / 4096")

    bestMatchedImagesFull.append(bestMatchedImagesPart)


if not endApp:
    newCompletedImage = imgForMosaic.copy()
    j = 0

    # Replacing the Tiles with the Pictures
    for i in range(64):
        for k in range(64):
            newCompletedImage[i*16:i*16+16,k*16:k*16+16] = bestMatchedImages[j]
            j = j+1


    # Displaying the Images
    cv2.namedWindow("Finished Image",cv2.WINDOW_GUI_NORMAL)
    cv2.namedWindow("Tile Image",cv2.WINDOW_GUI_NORMAL)
    cv2.imshow("Finished Image",newCompletedImage)
    cv2.setMouseCallback('Finished Image', click)

    print("To Save the Mosaik, press 'T'")

    # Loop for Image selection
    while True:
        key = cv2.waitKey(1) & 0xFF

        # Quitting
        if (key == ord("q")):
            break

        # Save Function
        if (key == ord("t")):
            cv2.imwrite("Exercise 4/bilder/Mosaik.png",newCompletedImage)
            print("Saved Mosaik")

        # Displaying the Clicked Image
        if(click_x <= 63 and click_y <= 63):
            cv2.imshow("Tile Image",bestMatchedImagesFull[click_y][click_x-1])

cv2.destroyAllWindows()


# file_name = './data/data16.npz'
# root_path = './data/101_ObjectCategories/'