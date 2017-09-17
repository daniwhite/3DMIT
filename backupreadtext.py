##from PIL import Image
##import pytesseract
##import argparse
##import csv
##import cv2
##import os

##    code from internet:
##    # load the example image and convert it to grayscale
##    image = cv2.imread(filename)
##    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
##     
##    # check to see if we should apply thresholding to preprocess the
##    # image
##    if preprocess == "thresh":
##            gray = cv2.threshold(gray, 0, 255,
##                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
##     
##    # make a check to see if median blurring should be done to remove
##    # noise
##    elif preprocess == "blur":
##            gray = cv2.medianBlur(gray, 3)
##     
##    # write the grayscale image to disk as a temporary file so we can
##    # apply OCR to it
##    filename = "{}.png".format(os.getpid())
##    cv2.imwrite(filename, gray)
##
##    # load the image as a PIL/Pillow image, apply OCR, and then delete
##    # the temporary file
##    text = pytesseract.image_to_string(Image.open(filename))
##    os.remove(filename)
##    print(text)
##     
##    # show the output images
##    cv2.imshow("Image", image)
##    cv2.imshow("Output", gray)
##    cv2.waitKey(0)

##def readText(filename, preprocess = 'thresh'):
##    text = pytesseract.image_to_string(Image.open(filename))
##    os.remove(filename)
##    return text


# ---------------------
##def readText(filename):
##    pytesseract.pytesseract.run_tesseract(filename, 'output', lang=None, boxes=True, config="hocr")
##    boxes = []
##    with open('output.box', 'r') as f: # 'rb'???
##        reader = csv.reader(f, delimiter = ' ')
##        for row in reader:
##            if(len(row)==6):
##                boxes.append(row)
##
##    # Draw the bounding box
##    img = cv2.imread(filename)
####    img = cv2.cv.LoadImage(filename, CV_LOAD_IMAGE_GRAYSCALE)
##    h, w, _ = img.shape
##    for b in boxes:
##        img = cv2.rectangle(img,(int(b[1]),h-int(b[2])),(int(b[3]),h-int(b[4])),(255,0,0),2)
##
##    cv2.imshow('output', img)
##    cv2.waitKey(0)
# ---------------------
