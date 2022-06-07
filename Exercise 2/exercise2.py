import cv2
import numpy as np
import glob



# Function that adjust the Color mask
def change_Color():
    lower_color = np.array([hue - hue_range, saturation -
                            saturation_range, value - value_range])
    upper_color = np.array([hue + hue_range, saturation +
                            saturation_range, value + value_range])

    # convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # create a mask
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return mask


# Function that reads the Image and returns it+its parameters
def load_Image(imgNumber):
    if imgNumber > len(images):
        imgNumber = 1
    elif imgNumber < 1:
        imgNumber = len(images)
    print(imgNumber)
    img = images[imgNumber-1]
    height = img.shape[0]
    width = img.shape[1]
    last_dim = img.shape[-1]
    return (img, height, width, last_dim, imgNumber)

# Class for Easy  Color Access


class Color:
    def __init__(self, Name, Hue, Hue_range, Saturation, Saturation_Range, Value, Value_Range,  Shape, Roundness, Filter):
        self.Name = Name
        self.Hue = Hue
        self.Hue_Range = Hue_range
        self.Saturation = Saturation
        self.Saturation_Range = Saturation_Range
        self.Value = Value
        self.Value_Range = Value_Range
        self.Shape = Shape
        self.Roundness = Roundness
        self.Filter = Filter


# Array for all Usefull Colors
colorArray = [
    Color('Blue', 100, 10, 160, 100, 255, 100, 2, 0.5, ['erosion']),
    Color('Yellow', 27, 10, 155, 100, 255, 100, 0, 0.2, ['erosion', 'erosion', 'erosion', 'dilation']),
    Color('Red', 180, 10, 255, 94, 228, 101, 2, 0.5, ['dilation', 'closing']),
    Color('Pink', 0, 10, 47, 100, 255, 40, 2, 0.5, ['erosion', 'dilation', 'closing', 'erosion']),
    Color('White', 27, 10, 47, 100, 255, 20, 2, 0.5, ['opening']),
    Color('Green', 43, 10, 147, 100, 147, 100, 2, 0.5, ['erosion']),
    Color('Red-Alt', 165, 10, 205, 100, 155, 100, 2, 0.5, ['']),
    Color('Pink-Alt', 170, 10, 30, 40, 255, 40, 2, 0.5, ['']),
    Color(
        'White-alt', 0, 1, 0, 1, 255, 3, 0, 0.5,
        ['dilation', 'dilation', 'erosion', 'erosion', 'erosion', 'erosion', 'erosion', 'dilation', 'dilation',
         'dilation'])]


# Get Starting Values
collorNumber = 0

hue = colorArray[collorNumber].Hue
hue_range = colorArray[collorNumber].Hue_Range
saturation = colorArray[collorNumber].Saturation
saturation_range = colorArray[collorNumber].Saturation_Range
value = colorArray[collorNumber].Value
value_range = colorArray[collorNumber].Value_Range
filterList = colorArray[collorNumber].Filter
shape = colorArray[collorNumber].Shape
expected_roundness = colorArray[collorNumber].Roundness


# Get all Images
images = [cv2.imread(file, cv2.IMREAD_COLOR) for file in glob.glob('images\\chewing_gum_balls**.jpg')]

# Load the first Image
imgNumber = 1
(img, height, width, last_dim, imgNumber) = load_Image(imgNumber)

# create the first mask
mask = change_Color()


def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE


kernel_size = 3
kernel_shape = morph_shape(shape)



# dilation with parameters
def dilation(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.dilate(img, element)



# erosion with parameters
def erosion(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.erode(img, element)



# opening with parameters
def opening(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, element)



# closing with parameters
def closing(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, element)


red_BGR = (0, 0, 255)
green_BGR = (0, 255, 0)
blue_BGR = (255, 0, 0)
circle_size = 6
circle_thickness = 3


min_size = 10
found = True

while True:

    # Copys the Image and Mask for editing
    imgcopy = img.copy()
    newmask = mask.copy()

    # Goes trough the filterlist and morphs the mask
    for i in range(len(filterList)):
        if filterList[i] == 'opening':
            newmask = opening(newmask, kernel_size, kernel_shape)
        if filterList[i] == 'dilation':
            newmask = dilation(newmask, kernel_size, kernel_shape)
        if filterList[i] == 'closing':
            newmask = closing(newmask, kernel_size, kernel_shape)
        if filterList[i] == 'erosion':
            newmask = erosion(newmask, kernel_size, kernel_shape)

    # Gets all connected Components
    connectivity = 8
    (numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(newmask, connectivity, cv2.CV_32S)

    # goes through all (reasonable) found connected components
    numRejected = 1
    for i in range(1, numLabels):
        # check size and roundness as plausibility
        topx = stats[i, cv2.CC_STAT_LEFT]
        topy = stats[i, cv2.CC_STAT_TOP]
        statWidth = stats[i, cv2.CC_STAT_WIDTH]
        statHeight = stats[i, cv2.CC_STAT_HEIGHT]

        if statWidth < min_size or statHeight < min_size:
            numRejected += 1
            continue  # found component is too small to be correct
        if statWidth > statHeight:
            roundness = 1.0 / (statWidth/statHeight)
        elif statHeight > statWidth:
            roundness = 1.0 / (statHeight/statWidth)

        if (roundness < expected_roundness):
            numRejected += 1
            continue  # ratio of width and height is not suitable

        # find and draw center
        center = centroids[i]
        center = np.round(center)
        center = center.astype(int)
        cv2.circle(imgcopy, center, circle_size, red_BGR, circle_thickness)

        # find and draw bounding box
        cv2.rectangle(imgcopy, (topx, topy), (topx + statWidth, topy + statHeight), blue_BGR, 3)

    # test for the Found Gum-Balls
    if found:
        print('We have found ' + str(numLabels-numRejected) + ' ' + colorArray[collorNumber].Name + ' balls.')
        found = False

    # Displays the Image
    cv2.imshow('Original image', imgcopy)
    cv2.imshow('Masked Image', newmask)

    # Ends the Program
    key = cv2.waitKey(100)
    if key == ord('q'):
        break

    # Sets the next Image
    if key == ord('t'):
        imgNumber = imgNumber+1
        (img, height, width, last_dim, imgNumber) = load_Image(imgNumber)
        mask = change_Color()
        found = True

    # Sets the prevoius Image
    if key == ord('g'):
        imgNumber = imgNumber-1
        (img, height, width, last_dim, imgNumber) = load_Image(imgNumber)
        mask = change_Color()
        found = True

    # Changes The Color
    if key == ord('e'):
        collorNumber = collorNumber+1
        if(collorNumber > len(colorArray)-1):
            collorNumber = 0
        found = True

        hue = colorArray[collorNumber].Hue
        hue_range = colorArray[collorNumber].Hue_Range
        saturation = colorArray[collorNumber].Saturation
        saturation_range = colorArray[collorNumber].Saturation_Range
        value = colorArray[collorNumber].Value
        value_range = colorArray[collorNumber].Value_Range
        filterList = colorArray[collorNumber].Filter
        shape = colorArray[collorNumber].Shape
        expected_roundness = colorArray[collorNumber].Roundness

        mask = change_Color()

    # Outputs all Stats
    if key == ord('n'):
        print('Hue: '+str(hue))
        print('Hue-Range : '+str(hue_range))
        print('Saturation : '+str(saturation))
        print('Saturation-Range : '+str(saturation_range))
        print('Value: '+str(value))
        print('Value-Range : '+str(value_range))
        print('Shape : '+str(shape))
        print('Roundness : '+str(expected_roundness))
        print('Filter: '+str(filterList))

# Kills the Application
cv2.destroyAllWindows()
