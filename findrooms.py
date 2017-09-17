import cv2
import numpy as np
import os

default_filepath = '../1_3.png'
MIN_AREA = 500  # Could be tuned
MAX_AREA = 20000  # Could be tuned
DOOR_THRESHOLD = 8*10**5  # Tuned
STAIR_THRESHOLD = 3*10**6
WORD_THRESHOLD = 10*10**5

# Set up template paths
template_folder = 'NumberImages'

def find_match(img, number, draw=False):
    """Find the number of doors in a floorplan."""
    w, h = 0, 0
    match, w, h = match_template(img, number, WORD_THRESHOLD, draw)
    return doors, w, h


def match_template(img, template_path, threshold, draw=False):
    """Find an arbitrary image within another image any number of times."""
    temp = cv2.imread(template_path, 0)
    w, h = temp.shape[::-1]

    # Find occurrences
    result = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF)

    # Threshold occurrences to only those that are accurate enough
    loc = np.where(result >= threshold)
    pts = []

    # Collect coordinates of doors and add them to return value array
    for pt in zip(*loc[::-1]):
        pts.append(pt)
        if draw:
            cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (125, 125, 0), 2)
    return pts, w, h

def findRooms(filename):
    res = []
    listing = os.listdir('/Users/jennahimawan/HackMIT/NumberImages/' + filename) 
    for number in listing:
        res.append(find_match('/Users/jennahimawan/Desktop/1_0.pdf', '/Users/jennahimawan/HackMIT/NumberImages/' + filename + '/' + number))

findRooms('1_0')

if __name__ == "__main__":
    min_area = int(input("Min area: "))
    max_area = int(input("Max area: "))
    path = input("Filepath: ")
    contours = find_room_contours(min_area, max_area, path)

    # Array of colors to cycle through
    colors = [(0, 255, 0), (0, 255, 255), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

    img = cv2.imread(path)

    # Draw contours in different colors
    for i in range(len(contours)):
        cnt = contours[i]
        img = cv2.drawContours(img, [cnt], -1, colors[i % len(colors)], 1)

    # Show image
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
