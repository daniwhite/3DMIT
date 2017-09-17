import cv2
import numpy as np

default_img_path = '../1_3.png'
door_paths = ['door_up_left.png', 'door_up_right.png', 'door_down_left.png', 'door_down_right.png', 'door_right_up.png',
              'door_right_down.png', 'door_left_up.png', 'door_left_down.png']  # All eight door configs
DEFAULT_THRESHOLD = 8*10**5  # Tuned


def match_template(img, template_path, threshold=DEFAULT_THRESHOLD, draw=False):
    """"Find an arbitrary image within another image any number of times."""
    temp = cv2.imread(template_path, 0)
    w, h = temp.shape[::-1]

    # Find occurrences
    result = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF)
    
    # Threshold occurrences to only those that are accurate enough
    loc = np.where(result >= threshold)
    pts = []

    # Collect coordinates of doors and add them to return value arraw
    for pt in zip(*loc[::-1]):
        pts.append(pt)
        if draw:
            cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (125, 125, 0), 2)
    return pts


def find_doors(img, threshold=DEFAULT_THRESHOLD, draw=False):
    """Find the number of doors in a floorplan."""
    for door_path in door_paths:
        match_template(img, door_path, threshold, draw)


if __name__ == "__main__":
    img = cv2.imread(default_img_path, 0)
    find_doors(img, DEFAULT_THRESHOLD, True)

    # Show image
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
