#!/usr/bin/env python
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('ss.png', 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bw = cv2.Canny(gray, 0, 50, 5);

#plt.imshow(img, interpolation='bicubic')
#plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
#plt.show()

#plt.imshow(gray, interpolation='bicubic')
#plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
#plt.show()

#plt.imshow(bw, interpolation='bicubic')
#plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
#plt.show()

hex = []

contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
	cnt_len = cv2.arcLength(cnt, True)
	# Ramer-Douglas-Peucker algorithm
	cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
	if len(cnt) == 6 and cv2.contourArea(cnt) > 5000 and cv2.isContourConvex(cnt):
		# detec angles
		hex.append(cnt)

cv2.drawContours(img , hex, -1, (0, 255, 0), 3 )
plt.imshow(img, interpolation='bicubic')
plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
plt.show()
