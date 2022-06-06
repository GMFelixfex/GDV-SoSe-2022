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

# Click Function, to Select an Image to display
def click(event, x, y, flags, param):
    global click_x
    global click_y
    global bigImage 

    if event == cv2.EVENT_LBUTTONDOWN:
        click_x = int(round(x,0)/16)
        click_y = int(round(y,0)/16)
        bigImage = int(round((((click_y) + 50*(click_x))/2550)*2500,0))


# Setting up the Training Data
root_path = 'Exercise 4/data/101_ObjectCategories/'  
file_name = 'Exercise 4/data/data16.npz'

trainData = TrainingSet(root_path)

# Decide if you want to Train or Load the Data
print("If you want to load instead of Training, press T")
key = cv2.waitKey() & 0xFF
if (key == ord("t")):
    trainData.loadTrainingData(file_name)
else:
    trainData.createTrainingData(Descriptor.TINY_COLOR16)
    trainData.saveTrainingData(file_name)

# Loading the Image
imgForMosaic =  cv2.imread('Exercise 4/bilder/cat2.png', cv2.IMREAD_COLOR)
imgForMosaic =  cv2.resize(imgForMosaic,(800,800))

# Dividing the Image in 2500 tiles
imgArray = []
for i in range(50):
    for k in range(50):
        imgArray.append(imgForMosaic[i*16:i*16+16,k*16:k*16+16])

bestMatchedImages = []
bestMatchedImagesFull = []
bestMatchedImagesPart=[]


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
    if(i%50 == 0 and i > 0):
        # Creating a 2d List
        bestMatchedImagesFull.append(bestMatchedImagesPart)
        bestMatchedImagesPart = []
    
    print("Picture Tile: "+str(i))
# bestMatchedImagesFull.append(bestMatchedImagesPart)


newCompletedImage = imgForMosaic.copy()
j = 0

# Replacing the Tiles with the Pictures
for i in range(50):
    for k in range(50):
        newCompletedImage[i*16:i*16+16,k*16:k*16+16] = bestMatchedImages[j]
        j = j+1


# Displaying the Images
cv2.namedWindow("Original Image",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Finished Image",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Possible Image",cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Original Image",imgForMosaic)
cv2.imshow("Finished Image",newCompletedImage)
cv2.setMouseCallback('Finished Image', click)

bigImage = 0

# Loop for Image selection
while True:
    key = cv2.waitKey(1) & 0xFF

    # Quitting
    if (key == ord("q")):
        break

    # Save Function
    if (key == ord("t")):
        cv2.imwrite("Exercise 4/bilder/Mosaik.png",newCompletedImage)

    # Displaying the Clicked Image
    if(click_x <= 49 and click_y <= 49):
        cv2.imshow("Possible Image",bestMatchedImagesFull[click_y][click_x-1])
