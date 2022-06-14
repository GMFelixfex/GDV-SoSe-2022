 
# GDV SoSe 2022: Exercise 4  
  

## About The Project   
  

This exercise is for the course "Grafische Datenverarbeitung" in the summer term of 2022 at HS Furtwangen University.  The whole project is written in Python via VS-Code   
    
  

## Prerequisites   
  

+ Python version 3.10.2   
	+ os
+ NumPy version 1.22.3   
+ OpenCv-python version  4.5.5   
+ GDV_TrainingSet.py
	+ pathlib
	+ glob
	+ enum



## Purpose   
  

The Application shows the usage of Image-Matching to create a Picture-Mosaik
The Picture-Mosaic has a size of 64x64 tiles (4096 pictures)
It uses Training data from ~9000 pictures and a FlannBasedMatcher to match tiles of the big image
  

## How to use   
  

1. The application can be started by opening the exercise4.py with VS-Code or the Python-launcher.   
2. In the Console you will be prompted to select the Training Descriptor with **"W"** or **"S"**, you can confirm the descriptor with **"D"**
3. Next you will be prompted to either press **"R"** to load the Trainingdata or any other key to train the data
4. You will now need to wait for the Program to finish generating the Mosaik (4096 PIctures, ~ 2-4min)
5. To end the application press **"Q"**.   
6. To save the Mosaik press **"T"**.   
7. To select a tile, just left-click it with the mouse cursor, it will then be displayed in the  "Tile-Image" window
    
  
  

## How does it work?   
    

In general, our project works like this:  
  
Step 1:  We open up a cv2 window and import the Image to use waitkey() for the selections and loading Process. The Image gets resized to 800x800

Step 2: We create an array of all descriptors and use a simple selection system to display the selected     		   		 descriptor

Step 3:  We check if there is already a dataset for the selected descriptor with os.path.isfile(), if not it will automatically start training 

 ```python
 if  os.path.isfile(file_name):
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

```

Step 4: We split the Image into 4096 tiles (16x16 size)

Step 5: We match a picture to every tile via the training data

 ```python
def  findBestMatch(trainData, sample):
	FLANN_INDEX_KDTREE = 1
	index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
	search_params = dict(checks=50)
	flann = cv2.FlannBasedMatcher(index_params, search_params)
	matches = flann.knnMatch(trainData.trainData, sample, k=1)
	matches = sorted(matches, key=lambda  x: x[0].distance)
	bestMatch = matches[0][0]
	return  bestMatch.queryIdx


for  i  in  range(len(imgArray)):
	newcomer = np.ndarray(shape=(1, descr.getSize()),
		buffer=np.float32(descr.compute(imgArray[i])),
		dtype=np.float32)
	idx = findBestMatch(trainData, newcomer)
	matchedImage = cv2.imread(trainData.getFilenameFromIndex(idx), cv2.IMREAD_COLOR)

```

Step 6:  We add the resulting picture to a 1d- and  2d-array. The 1d array stores all pictures resized to 16x16 while the pictures in the 2d array stay at full resolution

 ```python
	bestMatchedImages.append(cv2.resize(matchedImage,(16,16)))
	bestMatchedImagesPart.append(matchedImage)
	
	if(i%50 == 0  and  i > 0):
			bestMatchedImagesFull.append(bestMatchedImagesPart)
			bestMatchedImagesPart = []
	key = cv2.waitKey(1) & 0xFF
	
	if (key == ord("q")):
		endApp = True
		break
	print("Picture Tile: "+str(i))

bestMatchedImagesFull.append(bestMatchedImagesPart)
```

Step 7: We reform an Image with the new 16x16 pictures, to create and then display the mosaic

 ```python
for  i  in  range(50):
		for  k  in  range(50):
			newCompletedImage[i*16:i*16+16,k*16:k*16+16] = bestMatchedImages[j]
			j = j+1

cv2.namedWindow("Finished Image",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Tile Image",cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Finished Image",newCompletedImage)
```

Step  8: We set a mouse callback for interacting with the mosaic. When using the left click you can select an image to display in the "Tile Image" window

 ```python
def  click(event, x, y, flags, param):
	global  click_x
	global  click_y
	if  event == cv2.EVENT_LBUTTONDOWN:
	click_x = int(round(x,0)/16)
	click_y = int(round(y,0)/16)


cv2.setMouseCallback('Finished Image', click)
```

Step 9: We create a loop to display the selected tile and save the mosaic

 ```python
while True:
	key = cv2.waitKey(1) & 0xFF
	if (key == ord("q")):
			break
	if (key == ord("t")):
			cv2.imwrite("Exercise 4/bilder/Mosaik.png",newCompletedImage)
	if(click_x <= 49  and  click_y <= 49):
			cv2.imshow("Tile Image",bestMatchedImagesFull[click_y][click_x-1])
```

---  