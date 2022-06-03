from GDV_TrainingSet import Descriptor, TrainingSet
import cv2
import numpy as np


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
def click(event, x, y, flags, param):
    # grab references to the global variables
    global click_x
    global click_y
    global bigImage 

    if event == cv2.EVENT_LBUTTONDOWN:
        click_x = int(round(x,0)/16)
        click_y = int(round(y,0)/16)
        print(str(click_x)+" "+str(click_y))
        bigImage = int(round((((click_y) + 50*(click_x))/2550)*2500,0))

''' Define and compute or load the training data '''
root_path = 'Exercise 4/data/101_ObjectCategories/'  # adjust this path if you have the files in some other folder
# root_path = './data/temp/'  # you can use a smaller subset of the training data during development to save time
file_name = 'Exercise 4/data/data16.npz'
trainData = TrainingSet(root_path)
# either create and save the data
# trainData.createTrainingData(Descriptor.TINY_COLOR16)
# trainData.saveTrainingData(file_name)
# or load the saved data if descriptor has not been changed.
trainData.loadTrainingData(file_name)





imgForMosaic =  cv2.imread('Exercise 4/bilder/cat2.png', cv2.IMREAD_COLOR)
imgForMosaic =  cv2.resize(imgForMosaic,(800,800))

imgArray = []
# Note to remember: IMG[von-höhe:bis-höhe, von-breite:bis-breite]
# for i in range(10):
#    for k in range(10):
#        imgArray.append(imgForMosaic[i*8:i*8+8,k*8:k*8+8])

for i in range(50):
    for k in range(50):
        imgArray.append(imgForMosaic[i*16:i*16+16,k*16:k*16+16])

bestMatchedImages = []
bestMatchedImagesFull = []
bestMatchedImagesPart=[]

assert(isinstance(trainData.descriptor, Descriptor))
descr = trainData.descriptor
for i in range(len(imgArray)):
    newcomer = np.ndarray(shape=(1, descr.getSize()),
                      buffer=np.float32(descr.compute(imgArray[i])),
                      dtype=np.float32)
    idx = findBestMatch(trainData, newcomer)
    matchedImage = cv2.imread(trainData.getFilenameFromIndex(idx), cv2.IMREAD_COLOR)
    bestMatchedImages.append(cv2.resize(matchedImage,(16,16)))
    bestMatchedImagesPart.append(matchedImage)
    if(i%50 == 0 and i > 0):
        bestMatchedImagesFull.append(bestMatchedImagesPart)
        bestMatchedImagesPart = []
    
    print("Bild Teil: "+str(i))
bestMatchedImagesFull.append(bestMatchedImagesPart)

newCompletedImage = imgForMosaic.copy()
j = 0
#for i in range(10):
#    for k in range(10):
#        newCompletedImage[i*8:i*8+8,k*8:k*8+8] = bestMatchedImages[j]
#        j = j+1

for i in range(50):
    for k in range(50):
        newCompletedImage[i*16:i*16+16,k*16:k*16+16] = bestMatchedImages[j]
        j = j+1

#for i in range(80):
#    for k in range(80):
#        newCompletedImage[i:i+1,k:k+1] = bestMatchedImages[j]
#        j = j+1

cv2.namedWindow("Original Image",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Finished Image",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Possible Image",cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Original Image",imgForMosaic)
cv2.imshow("Finished Image",newCompletedImage)
cv2.setMouseCallback('Finished Image', click)

bigImage = 1200

while True:
    if(click_x <= 49 and click_y <= 49):
        cv2.imshow("Possible Image",bestMatchedImagesFull[click_y][click_x-1])

    key = cv2.waitKey(1) & 0xFF
    
    if (key == ord("w")):
        bigImage = bigImage+1
        print("Selected image: "+str(bigImage))
    if (key == ord("s")):
        bigImage = bigImage-1
        print("Selected image: "+str(bigImage))
    if (key == ord("q")):
        break
    if (key == ord("t")):
        cv2.imwrite("Exercise 4/bilder/Mosaik.png",newCompletedImage)

