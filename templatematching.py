import cv2
import numpy as np

default_img_path = '../1_3.png'

# Set up template paths
template_folder = 'template_imgs'
door_paths = [ template_folder + '/door_up_left.png', template_folder + '/door_up_right.png',
               template_folder + '/door_down_left.png', template_folder + '/door_down_right.png',
               template_folder + '/door_right_up.png', template_folder + '/door_right_down.png',
               template_folder + '/door_left_up.png', template_folder + '/door_left_down.png']  # All eight door configs
stair_paths = [template_folder + '/stairs_vertical.png', template_folder + '/stairs_horizontal.png', template_folder +
               '/stair_arrow_horizontal.png', template_folder + '/stair_arrow_vertical.png'] # Different stair selectors
DOOR_THRESHOLD = 8*10**5  # Tuned
STAIR_THRESHOLD = 3*10**6


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


def find_doors(img, draw=False):
    """Find the number of doors in a floorplan."""
    doors = []
    w, h = 0, 0
    for door_path in door_paths:
        doors_i = match_template(img, door_path, DOOR_THRESHOLD, draw)
        for door_i in doors_i:
            doors.append(door_i)
    return doors, w, h


def find_stairs(img, min_distance, draw=False):
    stairs = []
    w, h = 0, 0
    for stair in stair_paths:
        stairs_i, w, h = match_template(img, stair, STAIR_THRESHOLD, draw)
        for stair_i in stairs_i:
            stairs.append(stair_i)

    #Make sure none of the stairs points are repeated/too close
    ret_stairs = []
    for stair in stairs:
        for ret_stair in ret_stairs:
            if not (((ret_stair[0] - stair[0])**2 + (ret_stair[1] - stair[1])**2)**0.5 > min_distance):
                break
        else:
            ret_stairs.append(stair)
    return ret_stairs, w, h


if __name__ == "__main__":
    img = cv2.imread(default_img_path, 0)
    stairs, stair_w, stair_h = find_stairs(img, 50, False)

    for stair in stairs:
        cv2.rectangle(img, stair, (stair[0] + 2, stair[1] + 2), (125, 125, 0), 2)

    cv2.imwrite('out.png', img)

    # Show image
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
