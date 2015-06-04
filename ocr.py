#!/usr/bin/env python
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
import Image

def decode_tiles(img):
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	bw = cv2.Canny(gray, 0, 50, 5);

	## Show original image
	#plt.imshow(img, interpolation='bicubic')
	#plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
	#plt.show()

	## Show grayscale image
	#plt.imshow(gray, interpolation='bicubic')
	#plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
	#plt.show()

	## Show black/white image
	#plt.imshow(bw, interpolation='bicubic')
	#plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
	#plt.show()

	hex = []

	contours, hierarchy = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		cnt_len = cv2.arcLength(cnt, True)
		# Ramer-Douglas-Peucker algorithm
		cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
		if len(cnt) == 6 and cv2.contourArea(cnt) > 5000 and cv2.isContourConvex(cnt):
			# TODO: detect angles
			hex.append(cnt)

	## Draw contour lines
	cv2.drawContours(img , hex, -1, (0, 255, 0), 3 )
	plt.imshow(img, interpolation='bicubic')
	plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
	#plt.show()

	## Show isolated contours
	plt.figure()
	h,w,d = img.shape
	mask = np.zeros((h,w), np.uint8)
	cv2.drawContours(mask, hex, -1, 255, -1)
	crop = cv2.bitwise_and(img, img, mask=mask)
	plt.imshow(crop, interpolation='bicubic')
	plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
	plt.show()

	hexx = []

	# Process hexagons
	for cnt in hex:
		# Build mask
		h,w,d = img.shape
		mask = np.zeros((h,w), np.uint8)
		cv2.drawContours(mask, [cnt], 0, 255, -1)
		crop = cv2.bitwise_and(img, img, mask=mask)

		shape_descriptor = {}

		# OCR
		crop_t = Image.fromarray(crop)
		shape_descriptor['letter'] = pytesseract.image_to_string(crop_t, config="-psm 10")

		# determine team
		mean_color = cv2.mean(img, mask)
		if (mean_color[0] > mean_color[2]*1.5): # redder than it is blue
			shape_descriptor['team'] = 'red'
		elif (mean_color[2] > mean_color[0]*1.5): # bluer than it is red
			shape_descriptor['team'] = 'blue'
		else:
			shape_descriptor['team'] = 'none'
		
		# determine if it is a capital
		cropgray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
		num_white_pixels = np.sum(cropgray > 225)
		shape_descriptor['capital'] = 0
		if (num_white_pixels > 500 and shape_descriptor['team'] != 'none'):
			shape_descriptor['capital'] = 1

		# find center
		m = cv2.moments(mask, True)
		center = {'x': m['m10']/m['m00'], 'y': m['m01']/m['m00']}
		hexgrid = hexagonal_grid(center)
		shape_descriptor['i'] = hexgrid['i']
		shape_descriptor['j'] = hexgrid['j']

		hexx.append(shape_descriptor)
		#plt.imshow(crop, interpolation='bicubic')
		#plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
		#plt.show()
	return hexx

def hexagonal_grid(center):
	orig_x = 374
	orig_y = 854
	hy = 120
	sx = 100
	sy = 65

	# Map to hexagonal coordinates
	# I'm not proud of this
	coords = []
	for eye in np.arange(-3,4):
		for jay in np.arange(-3,4):
#			y = orig_y + jay*(np.sqrt(3)*s) + eye*(2.0/np.sqrt(2)*s)
#			x = orig_x + eye*(2.0/np.sqrt(2)*s)
			y = orig_y + jay*hy + eye*sy
			x = orig_x + eye*sx
			coords.append((x,y,eye,jay))

	min = (100000, 0, 0)
	myx = center['x']
	myy = center['y']
	for c in coords:
		dist = np.sqrt((myx - c[0])**2 + (myy - c[1])**2)
		if dist < min[0]:
			min = (dist, c[2], c[3])

	return {'i': min[1], 'j': min[2]}


screenshot = cv2.imread('ss.png', 1)
grid = decode_tiles(screenshot)
