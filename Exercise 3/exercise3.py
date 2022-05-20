from cv2 import Laplacian
import numpy as np
import cv2

# Array for Clicking position
ref_pt_src = []
ref_pt_dst = []

# Function for clicking on the 1st image
def clickSrc(event, x, y, flags, param):
    global ref_pt_src
    global colorSelection1
    if event == cv2.EVENT_LBUTTONDOWN:
        colorSelection1 = colorSelection1+1
        pos = len(ref_pt_src)
        if (pos == 0):
            ref_pt_src = [(x, y)]
        else:
            ref_pt_src.append((x, y))

# Function for clicking on the 2nd image
def clickDst(event, x, y, flags, param):
    global ref_pt_dst
    global colorSelection2
    if event == cv2.EVENT_LBUTTONDOWN:
        colorSelection2 = colorSelection2+1
        pos = len(ref_pt_dst)
        if (pos == 0):
            ref_pt_dst = [(x, y)]
        else:
            ref_pt_dst.append((x, y))

# Function for Calculating an image with a full kernel
def convolution_with_opencv(image, kernel):
    kernel = cv2.flip(kernel, -1)
    ddepth = -1
    output = cv2.filter2D(image, ddepth, kernel)
    return output


# Calculation based on our Own Tutorial convolution_with_opencv()
def hybrid_with_kernel_solution(img_1, img_2, kernelSize, _sigma):
    #Gaussian Kernel
    kernel1D1 = cv2.getGaussianKernel(kernelSize, _sigma)
    kernel1 = np.transpose(kernel1D1) * kernel1D1

    #Unit Impulse Kernel
    kernel1D2 = cv2.getGaussianKernel(kernelSize, 0.9)
    kernel2 = np.transpose(kernel1D2) * kernel1D2

    #Laplacian Kernel
    kernel3 = cv2.subtract(kernel1,kernel2)

    img_1 = convolution_with_opencv(img_1,kernel1)
    img_2 = convolution_with_opencv(img_2,kernel3)
    img_3 = cv2.add(img_1,img_2)

    return img_1, img_2, img_3

# Calculation based on our Own Tutorial convolution_with_opencv(), as well as a premade Laplacian Kernel
def hybrid_with_premade_kernel(img_1, img_2, kernelSize, _sigma):

    #Gaussian Kernel
    kernel1D1 = cv2.getGaussianKernel(kernelSize, _sigma)
    kernel1 = np.transpose(kernel1D1) * kernel1D1

    #Laplacian Kernel
    myownKernel = [[1,1,1],[1,-8,1],[1,1,1]]
    kernel3=  np.array(myownKernel)

    img_1 = convolution_with_opencv(img_1,kernel1)
    img_2 = convolution_with_opencv(img_2,kernel3)
    img_3 = cv2.add(img_1,img_2)

    return img_1, img_2, img_3

# Caculation based of GaussianBlur() and Laplacian()
def  hybrid_with_premade_functions(img_1,img_2,kernelSize,_sigma):
    img_1 = cv2.GaussianBlur(img_1, (kernelSize,kernelSize), _sigma)
    kernelSize = 3
    img_2 = cv2.Laplacian(img_2,-1,ksize=kernelSize,)
    img_3 = cv2.add(img_1,img_2)

    return img_1, img_2, img_3

# Caculation based of GaussianBlur() with Unit Impuls
def hybrid_with_adjusted_functions(img_1,img_2,kernelSize,_sigma):
    img_1 = cv2.GaussianBlur(img_1, (kernelSize,kernelSize), _sigma)
    img_2 = cv2.subtract(cv2.GaussianBlur(img_2, (kernelSize,kernelSize), _sigma), cv2.GaussianBlur(img_2, (kernelSize,kernelSize),1, 0.9))
    
    img_3 = cv2.add(img_1,img_2)
    return img_1, img_2, img_3


# Caculation based of GaussianBlur() with Unit Impuls, adjusted to a higher brightness 
def hybrid_with_adjusted_functions_and_brightness(img_1,img_2,kernelSize,_sigma):
    img_1 = cv2.GaussianBlur(img_1, (kernelSize,kernelSize), _sigma)
    img_2 = cv2.subtract(cv2.GaussianBlur(img_2, (kernelSize,kernelSize), _sigma), cv2.GaussianBlur(img_2, (kernelSize,kernelSize),1, 0.9))-127
    
    img_3 = cv2.add(img_1//2,img_2//2)
    return img_1, img_2, img_3


# Load image and resize for better display
img1 = cv2.imread('images\\dog.bmp', cv2.IMREAD_COLOR)
rows, cols , dims= img1.shape

img2 = cv2.imread('images\\cat.bmp', cv2.IMREAD_COLOR)
img2 = cv2.resize(img2, (cols, rows), interpolation=cv2.INTER_CUBIC) 

# Varibale to select the type of laplacian and gaussian calculation
calcType = 0

# Colorarray for the circles
colors = [(255,0,0),(0,255,0),(0,0,255),(255,0,0),(0,255,0),(0,0,255)]
colorSelection1 = 0
colorSelection2 = 0

# Window Setup
cv2.namedWindow('Original 1 with Input')
cv2.setMouseCallback('Original 1 with Input', clickSrc)
cv2.namedWindow('Original 2 with Input')
cv2.setMouseCallback('Original 2 with Input', clickDst)


# Sigma and KernelSize for calculations
sigma = 6
kernel_size = 15

# Names of the caculation types
calcTypeNames = ["hybrid_with_kernel_solution","hybrid_with_premade_kernel","hybrid_with_premade_functions","hybrid_with_adjusted_functions","hybrid_with_adjusted_functions_and_brightness"]

img2_transform = img2.copy()
computationDone = False
while True:

    # Copy of all needed Images
    img1_copy = img1.copy()
    img2_copy = img2_transform.copy()
    img1_circle = img1.copy()
    img2_circle = img2.copy()

    # Forces 3 circles
    if(len(ref_pt_src) > 3):
        ref_pt_src.pop(0)
        computationDone = False

    if(len(ref_pt_dst) > 3):
        ref_pt_dst.pop(0)
        computationDone = False

    # Draws 3 circles
    for i in range(len(ref_pt_src)):
        cv2.circle(img1_circle, ref_pt_src[i], 4, colors[i+(colorSelection1%3)], 2) 
    for i in range(len(ref_pt_dst)):
        cv2.circle(img2_circle, ref_pt_dst[i], 4, colors[i+(colorSelection2%3)], 2)



    # Computes transform
    if not(computationDone) and (len(ref_pt_src) == 3 and len(ref_pt_dst) == 3):
        T_affine = cv2.getAffineTransform(np.float32(ref_pt_dst), np.float32(ref_pt_src))
        img2_transform = cv2.warpAffine(img2.copy(), T_affine, (cols, rows))
        computationDone = True




    # Decides the type of calculation to be used
    if calcType == 0:
        gausImg, lapImg, hydridImg = hybrid_with_kernel_solution(img1_copy.copy(),img2_copy.copy(),kernel_size,sigma)

    elif calcType == 1:
        gausImg, lapImg, hydridImg = hybrid_with_premade_kernel(img1_copy.copy(),img2_copy.copy(),kernel_size,sigma)

    elif calcType == 2:
        gausImg, lapImg, hydridImg = hybrid_with_premade_functions(img1_copy.copy(),img2_copy.copy(),kernel_size,sigma)

    elif calcType == 3:
        gausImg, lapImg, hydridImg = hybrid_with_adjusted_functions(img1_copy.copy(),img2_copy.copy(),kernel_size,sigma)

    elif calcType == 4:
        gausImg, lapImg, hydridImg = hybrid_with_adjusted_functions_and_brightness(img1_copy.copy(),img2_copy.copy(),kernel_size,sigma)



    # Displaying the different images
    cv2.imshow("Original 1 with Input",img1_circle)
    cv2.imshow("Original 2 with Input",img2_circle)
    cv2.imshow("Transformed Image 2",img2_copy)
    cv2.imshow("Gaus",gausImg)
    cv2.imshow("Laplacian",lapImg)
    cv2.imshow("Hybrid",hydridImg)


    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the transformation
    if key == ord("r"):
        ref_pt_src = []
        ref_pt_dst = []
        computationDone = False

    #   if the 'w' key is pressed, loop through the calculation types
    if key == ord("w"):
        calcType = calcType+1
        if calcType > 4:
            calcType = 0
        print(calcTypeNames[calcType])


    # if the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break