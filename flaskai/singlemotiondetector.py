
import numpy as np
import imutils
import cv2

class SingleMotionDetector:
    def __init__(self, accumWeight=0.5):
        # store the accumulated weight factor
        self.accumWeight = accumWeight

        # initialize the background model ...
        self.bg = None

    # update method will accept an input frame and compute the
    # weighted avarage

    def update(self, image):
        # if the background model is None, initialize it
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        # update the background model by accumulating the weighted average

        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    # Given our background bg we can now apply motion detection via the
    # detect method

    def detect(self, image, tVal=25):
        # compute the absolute difference between the background model
        # and the image passed in , then threshold the delta image

        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta,tVal,255, cv2.THRESH_BINARY)[1]

        # perform a series of erosions and dialtion to remove small blobs

        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Applying contour detection to extract any motion regions
        # find contours in the thresholded image and initialize the
        # minimum and maximum bounding box regions formotion

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
         cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        # Populate these variables (minX minY ...) , (provided motion
        # exists in the frame )

        # if no contours were fornd, return None. in this case there was
        # no motion found in the frame and we can safely ignore it.
        if len(cnts) == 0:
            return None

        # otherwise, loop over th contours

        for c in cnts:
            # compute the bounding box of the contour and use it to
            # update the minimum and maximum bounding box regions
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX,x),min(minY,y))
            (maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))


        # otherwise, return a tuple of the threshold image along
        # with bounding box
        return (thresh,(minX, minY, maxX, maxY))
