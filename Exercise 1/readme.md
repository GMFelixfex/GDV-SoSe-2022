# GDV SoSe 2022: Exercise 1
## About The Project
This exercise is for the course "Grafische Datenverarbeitung" in the summer term 2022 at HS Furtwangen University.  The whole project is written in Python via VS-Code

## Prerequisites
+ Python version 3.10.2
	+ Operator
	+ Math
+ NumPy version 1.22.3
+ OpenCv-python version  4.5.5

## Purpose
The  Application shows the **Luminance-gradient-dependent lightness illusion** via a simple animation made with OpenCV. 
The **Luminance-gradient-dependent lightness illusion** is a illusion about the different ways to percieve the same color / shade of gray, when put agaisnt a different colored background.

To illustrate the difference, we used two boxes in the corner of the animation.
The third box is passing between the other ones, even overlapping at some point, to show the matching color.
## How to use
1. The application  can be started by opening the ubung1.py with VS-Code or the Python-launcher.
2. The animation will start automatically.
3. Tho end the animation, press **"Q"**.
4. You will shortly after be promted to either use **"W"** to exit the application or **"E"** to export the animation progress to a **.mp4** file.
5. The file can be found in /videos with the name Test.mp4
## How does it work?
1. We create an empty grayscale image with:
	~~~python 
	img = np.zeros((100, 256, 1), np.uint8) 
	~~~
2. We get the Height  and Width Component of he image
3. We create Variables to time/store/regulate the animation
4. We create a while-loop for generating the individual frames
5. We generate  a gradient with:
	```python 
	for i in range(height):
		for j in range(width):
			img[i][j] = j
	```
6. We resize the frame to 16x the original size and the get new dimensions
7. We copy a 4x4 area in the middle of the frame and resize it to 50x50:
	```python 
	small_square = img_alt[height2//2-2:height2//2+2,
							width2//2-2:width2//2+2]
	small_square = cv2.resize(small_square, (0,0), fx=12.5, fy=12.5)
	```
8. We get the path of the moving square with:
	```python 
	def circle_path(t, scale, offsetY, offsetX):
		res = (int(scale*math.cos(t)+offsetX),
			   int(scale*math.sin(t)+offsetY))
		return  res
	pt1 = circle_path(timer, 600, -300, width2//2-20)
	```
9. We map the path to an area of 50x50:
	```python 
	size = (50, 50)
	pt2 = tuple(map(op.add, pt1, size))
	``` 
10.  We set the position of the `small_square` to the newly mapped positions
	```python 
	img_alt[pt1[1]:pt2[1], pt1[0]:pt2[0]] = small_square
	``` 
11. We determine the direction of the movement and increment the timer
	```python 
	if (timer <= -5.6  or  timer >= -3.8):
		timer_increment = -timer_increment
	timer += timer_increment
	```
12. We paste the `small_square` into both upper corners of the animation
13. We display and store the image in the `img_array` list
14. We can now decide to exit the animation with **Q** which will also save the framesize
15. We create a temporary image to inform the user, if he wants to exist the application or save the video
16. At last we create a loop to write all frames to a video file and svae it in `/videos/test.mp4`
---
