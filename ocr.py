#!/usr/bin/env python
import cv2
import numpy as np
import pytesseract
import Image

# Find the (x,y) centroid of a polygon (cnt) in img
def get_center(cnt, img):
    h,w,d = img.shape
    mask = np.zeros((h,w), np.uint8)
    cv2.drawContours(mask, [cnt], 0, 255, -1)
    m = cv2.moments(mask, True)
    return (m['m10']/m['m00'], m['m01']/m['m00'])
        
def decode_tiles(img):
    # Greyscale and edge detection
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    bw = cv2.Canny(gray, 0, 50, 5);

    # HACK: some thresholds for hexagon recognition
    h,w,d = img.shape
    img_area = h*w
    hex_area = img_area / 200
    cap_area = img_area / 2000

    hex = []

    contours, hierarchy = cv2.findContours(
        bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Discard contours which don't seem like large-ish hexagons
    for cnt in contours:
        # Ramer-Douglas-Peucker algorithm
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)

        if (len(cnt) == 6 and \
            cv2.contourArea(cnt) > hex_area and \
            cv2.isContourConvex(cnt)):
            # more robust: check angles for regularity ~ 120 deg.
            # does not seem to be necessary
            hex.append(cnt)

    # Pick (x0,y0) origin for relative hex grid (arbitrary)
    origin = get_center(hex[0], img)

    # Estimate side length s
    num_hex = 0
    s = 0
    for cnt in hex:
        ss = 0
        for k in range(0,4):
            ss += np.sqrt((cnt[k][0][0] - cnt[k+1][0][0])**2 + \
                         (cnt[k][0][1] - cnt[k+1][0][1])**2)
        # Sixth side
        ss += np.sqrt((cnt[5][0][0] - cnt[0][0][0])**2 + \
                         (cnt[5][0][1] - cnt[0][0][1])**2)
        s += (ss / 6)
        num_hex += 1

    s /= num_hex

    # Identify hexagons
    grid = []
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
        shape_descriptor['letter'] = shape_descriptor['letter'].lower()

        # determine team
        # recall OpenCV likes BGR
        mean_color = cv2.mean(img, mask)
        if (mean_color[0] > mean_color[2]*1.5): # much bluer than it is red
            shape_descriptor['team'] = 'blue'
        elif (mean_color[2] > mean_color[0]*1.5): # much redder than it is blue
            shape_descriptor['team'] = 'red'
        else:
            shape_descriptor['team'] = 'none'
        
        # determine if it is a capital
        cropgray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
        num_white_pixels = np.sum(cropgray > 225)
        shape_descriptor['capital'] = 0
        if (num_white_pixels > cap_area and shape_descriptor['team'] != 'none'):
            shape_descriptor['capital'] = 1

        # find center
        (x0,y0) = get_center(cnt, img)
        center = {'x': x0, 'y': y0}
        hexgrid = hexagonal_grid(center, origin, s)
        shape_descriptor['i'] = hexgrid['i']
        shape_descriptor['j'] = hexgrid['j']

        shape_descriptor['contour'] = cnt

        grid.append(shape_descriptor)
    return grid

# Translate rectangular coordinates to hexagonal coordinates (approx)
def hexagonal_grid(center, origin, s):
    (x0,y0) = origin
    s += 8  # FIXME
    b = 20

    h = np.sqrt(3)*s
    r = h/2.

    # Map to hexagonal coordinates (see hex_derivation.jpg)
    eye = (center['x'] - x0)/(s+1./2.*(b+s))
    jay = ((center['y'] - y0) - eye*(r+1./2.*b)) / (h+b)

    return {'i': int(round(eye)), 'j': int(round(jay))}
