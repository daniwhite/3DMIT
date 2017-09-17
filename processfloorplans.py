import cv2
import numpy as np

default_filepath = '../1_3.png'
MIN_AREA = 500  # Could be tuned
MAX_AREA = 20000  # Could be tuned
DOOR_THRESHOLD = 8*10**5  # Tuned
STAIR_THRESHOLD = 3*10**6

# Set up template paths
template_folder = 'template_imgs'
door_paths = [ template_folder + '/door_up_left.png', template_folder + '/door_up_right.png',
               template_folder + '/door_down_left.png', template_folder + '/door_down_right.png',
               template_folder + '/door_right_up.png', template_folder + '/door_right_down.png',
               template_folder + '/door_left_up.png', template_folder + '/door_left_down.png']  # All eight door configs
stair_paths = [template_folder + '/stairs_vertical.png', template_folder + '/stairs_horizontal.png', template_folder +
               '/stair_arrow_horizontal.png', template_folder + '/stair_arrow_vertical.png'] # Different stair selectors


def compute_edges(img, delta = 3):
    """Computer what doors connect what contours.

    :param delta: stepsize for iterating along door edge
    """
    doors, w, h = find_doors(img)
    contours = find_room_contours(MIN_AREA, MAX_AREA, default_filepath)
    edges = []
    for door in doors:
        initial_contour = -1
        for cnt in contours:
            if cv2.pointPolygonTest(cnt, door, False) < 0:
                continue
            else:
                initial_contour = cnt
                break
        if initial_contour == -1:
            continue
        pos = door
        while pos[0] < door[0] + w:
            for cnt in contours:
                if cv2.pointPolygonTest(cnt, door, False) < 0:
                    continue
                else:
                    current_contour = cnt
                    break
            if not (current_contour == initial_contour):
                edges.append((current_contour, initial_contour))


def compute_vertices(contours):
    """Create a dictionary with labels as keys and contours as values."""
    dict = {}
    for contour in contours:
        key = str((hex(sum(contour.flatten()))))
        dict[key] = contour
    return dict


def find_doors(img, draw=False):
    """Find the number of doors in a floorplan."""
    doors = []
    w, h = 0, 0
    for door_path in door_paths:
        doors_i = match_template(img, door_path, DOOR_THRESHOLD, draw)
        for door_i in doors_i:
            doors.append(door_i)
    return doors, w, h


def find_room_contours(min_area=MIN_AREA, max_area=MAX_AREA, path=default_filepath):
    """Find contours of the room."""
    img = cv2.imread(path)

    # Make all pixels that aren't pure white into black pixels
    ret, img2 = cv2.threshold(img, 254, 255, cv2.THRESH_TOZERO)
    # Ensure the image is black and white for finding contours
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    img2, contours, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    good_contours = []

    # Throw out contours that are too small
    for cnt in contours:
        if cv2.contourArea(cnt) > min_area and cv2.contourArea(cnt) < max_area:
            good_contours.append(cnt)
    return good_contours


def find_stairs(img, min_distance, draw=False):
    """Find all stairs in an image."""
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
