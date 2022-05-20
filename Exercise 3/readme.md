# GDV SoSe 2022: Exercise 3

## About The Project  

This exercise is for the course "Grafische Datenverarbeitung" in the summer term 2022 at HS Furtwangen University.  The whole project is written in Python via VS-Code  
  

## Prerequisites  

+ Python version 3.10.2  
+ NumPy version 1.22.3  
+ OpenCv-python version  4.5.5  
  

Project is Pep8-Formatted with the exeption of the Max-Line-Length.  

## Purpose  

The Application shows the usage of filtering on Images via **Gausian and Laplacian** filters.
The created Images are then combined to crate a so called **Hybrid Image**.

To make it more compatible with more images, we added an affine transformation calculation.


## How to use  

1. The application  can be started by opening the exercise3.py with VS-Code or the Python-launcher.  
2. To end the application, press **"Q"**.  
3. To change filter press **"W"**.  
4. To reset your transformation press **"R"**.  
5. To Transform the Image just **"Left-Click"** the **"Original 1 with Input"** and  **"Original 2 with Input"** window, on spots you want to match together
6. At max you can use  **three**  mathing spots, the oldest will get deleted
7. They are color coded to match each other
  

Everytime you Update the image or color, the new count of gumballs will be printed to the console.  
  

## How does it work?  
  
In general our project works like this:

1. Import two Images and resize them to fit each other
2. Tranform the second image with the affine transform
3. Use the Gaussian Blur on the First image
4. Use the Laplacian/Highpass on the second image
5. Combine both images
6. Show the images

Step 1 and 6 are self explanatory

Step 2 works by saving three point on each image to an array
```python
cv2.namedWindow('Original 1 with Input')
cv2.setMouseCallback('Original 1 with Input', clickSrc)

def  clickSrc(event, x, y, flags, param):
	global  ref_pt_src
	global  colorSelection1
	if  event == cv2.EVENT_LBUTTONDOWN:
		colorSelection1 = colorSelection1+1
		pos = len(ref_pt_src)
		if (pos == 0):
			ref_pt_src = [(x, y)]
		else:
			ref_pt_src.append((x, y))
```
The saved points are then used to calculate the affine transform which is then applied to the second image
```python
if  not(computationDone) and (len(ref_pt_src) == 3  and  len(ref_pt_dst) == 3):
    T_affine = cv2.getAffineTransform(np.float32(ref_pt_dst),
	    np.float32(ref_pt_src))
	img2_transform = cv2.warpAffine(img2.copy(), T_affine, (cols, rows))
	computationDone = True
```
Steps 3 to 5  are done together, by using various different methods:
Method 1: *Calculation based on our Own Tutorial convolution_with_opencv()*
```python
def  convolution_with_opencv(image, kernel):
	kernel = cv2.flip(kernel, -1)
	ddepth = -1
	output = cv2.filter2D(image, ddepth, kernel)
	return  output

def  hybrid_with_kernel_solution(img_1, img_2, kernelSize, _sigma):
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
	#Adding Together
	img_3 = cv2.add(img_1,img_2)
return  img_1, img_2, img_3
```
Method 2: *Calculation based on our Own Tutorial convolution_with_opencv(), as well as a premade Laplacian Kernel*
```python
def  convolution_with_opencv(image, kernel):
	kernel = cv2.flip(kernel, -1)
	ddepth = -1
	output = cv2.filter2D(image, ddepth, kernel)
	return  output

def  hybrid_with_premade_kernel(img_1, img_2, kernelSize, _sigma):
	#Gaussian Kernel
	kernel1D1 = cv2.getGaussianKernel(kernelSize, _sigma)
	kernel1 = np.transpose(kernel1D1) * kernel1D1
	#Laplacian Kernel
	myownKernel = [[1,1,1],[1,-8,1],[1,1,1]]
	kernel3= np.array(myownKernel)
	img_1 = convolution_with_opencv(img_1,kernel1)
	img_2 = convolution_with_opencv(img_2,kernel3)
	#Adding Together
	img_3 = cv2.add(img_1,img_2)
	return  img_1, img_2, img_3
```
Method 3: *Caculation based of cv2.GaussianBlur() and cv2.Laplacian()*
```python
	def  hybrid_with_premade_functions(img_1,img_2,kernelSize,_sigma):
	img_1 = cv2.GaussianBlur(img_1, (kernelSize,kernelSize), _sigma)
	kernelSize = 3
	img_2 = cv2.Laplacian(img_2,-1,ksize=kernelSize,)
	#Adding Together
	img_3 = cv2.add(img_1,img_2)
	return  img_1, img_2, img_3
```
Method 4: *Caculation based of cv2.GaussianBlur() with Unit Impuls*
```python
def  hybrid_with_adjusted_functions(img_1,img_2,kernelSize,_sigma):
	img_1 = cv2.GaussianBlur(img_1, (kernelSize,kernelSize), _sigma)
	img_2 = cv2.subtract(cv2.GaussianBlur(img_2, (kernelSize,kernelSize), _sigma), 
		cv2.GaussianBlur(img_2, (kernelSize,kernelSize),1, 0.9))
	#Adding Together
	img_3 = cv2.add(img_1,img_2)
	return  img_1, img_2, img_3
```
Method 5: *Caculation based of cv2.GaussianBlur() with Unit Impuls, adjusted to a higher brightness*
```python
def  hybrid_with_adjusted_functions(img_1,img_2,kernelSize,_sigma):
	img_1 = cv2.GaussianBlur(img_1, (kernelSize,kernelSize), _sigma)
	img_2 = cv2.subtract(cv2.GaussianBlur(img_2, (kernelSize,kernelSize), _sigma), 
		cv2.GaussianBlur(img_2, (kernelSize,kernelSize),1, 0.9))-127
	#Adding Together
	img_3 = cv2.add(img_1//2,img_2//2)
	return  img_1, img_2, img_3
```

Not all methods result in the same hybrid: method 1 and 4 are the only identical solutions, the others have a varying degree of success. 

Method 1 and 4 bring out the best solutions.
Method 2 has an extremly bright end result for the laplacian, which can be benefical, but in most cases is unwanted
Method 3 has almost the exact same result as method, but it is even brighter
Method 5 has a overall adjusted brightness to emulate, our research on the internet, the closest.




---