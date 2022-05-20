# GDV SoSe 2022: Exercise 2
## About The Project
This exercise is for the course "Grafische Datenverarbeitung" in the summer term 2022 at HS Furtwangen University.  The whole project is written in Python via VS-Code

## Prerequisites
+ Python version 3.10.2
	+ Glob
	+ Math
+ NumPy version 1.22.3
+ OpenCv-python version  4.5.5

Project is Pep8-Formatted with the exeption of the Max-Line-Length.
## Purpose
The  Application shows the usage of  **Morphologiccal Operations** via a Color Detection agorythm.

It should detect the **Amount and Position of all** the colored gumballs in the images from the image folder. It can determine the amount of Blue, Yellow, Green, (Red, Pink and White)x2 gumballs  depending on the lighting conditions.

## How to use
1. The application  can be started by opening the exercise2.py with VS-Code or the Python-launcher.
2. The application will start automatically.
3. Tho end the application, press **"Q"**.
4. To change the color press **"E"**.
5. To change the image use **"T"** and **"G"**.
6. To get the current HSV color and filter information Press **"N"**.
7. To change a color attribute or the Morphological-Operations,  edit the color in the `colorArray` List.

Everytime you Update the image or color, the new count of gumballs will be printed to the console.

## How does it work?

Too effectivly switch and store colors we used a class called `Color`
With the attributes: `Name` `Hue` `Hue_Range` `Saturation` `Saturation_Range` `Value` `Value_Range` `Shape` `Roundness` `Filter`.
It can store all the usefull information that the color needs to be identified.

+ We use the glob library to Import all the images to an Array.
	```python
	images = [cv2.imread(file, cv2.IMREAD_COLOR) for  file  in glob.glob('images\\chewing_gum_balls**.jpg')]
	```

+ We have a filterlist that get iterated to apply the different Mophological operation to the mask.
	```python
	for i in  range(len(filterList)):
		if filterList[i] == 'opening':
			newmask = opening(newmask, kernel_size, kernel_shape)
		if filterList[i] == 'dilation':
			newmask = dilation(newmask, kernel_size, kernel_shape)
		if filterList[i] == 'closing':
			newmask = closing(newmask, kernel_size, kernel_shape)
		if filterList[i] == 'erosion':
			newmask = erosion(newmask, kernel_size, kernel_shape)
	```
+ All returned components form the `cv2.connectedComponentsWithStats` function get evaluated in Roundness and Size, so we can eliminate straggling white pixels from the mask.
	```python
	for i in  range(1, numLabels):

	topx = stats[i, cv2.CC_STAT_LEFT]
	topy = stats[i, cv2.CC_STAT_TOP]
	statWidth = stats[i, cv2.CC_STAT_WIDTH]
	statHeight = stats[i, cv2.CC_STAT_HEIGHT]

	if statWidth < min_size or statHeight < min_size:
		numRejected += 1
		continue 
	if statWidth > statHeight:
		roundness = 1.0 / (statWidth/statHeight)
	elif statHeight > statWidth:
		roundness = 1.0 / (statHeight/statWidth)
	if (roundness < expected_roundness):
		numRejected += 1
		continue  
	```
+ The Mophological-Operations are programmed  with `cv2.morphologyEx`, `cv2.dilate` and `cv2.erode` function  while using a element from `cv2.getStructuringElement`Example:
	```python
	def  dilation(img, size, shape):
		element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
		return cv2.dilate(img, element)
	```

---

