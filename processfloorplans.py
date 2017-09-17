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
    contours = find_room_contours(img)
    edges = []

    for door in doors:
        find_contours_from_line(contours, edges, door, w, h, 'top', delta)
        find_contours_from_line(contours, edges, door, w, h, 'bottom', delta)
        find_contours_from_line(contours, edges, door, w, h, 'left', delta)
        find_contours_from_line(contours, edges, door, w, h, 'right', delta)

    return edges


def compute_vertices(contours):
    """Create a dictionary with labels and as keys and contours as values."""
    vertices = []
    for contour in contours:
        vertices.append(get_contour_label(contour))
    return vertices


def find_contours_from_line(contours, edges, orig_pos, w, h, side, delta=3):
    """"Iterate around the border of the door to find a new contour"""
    pos = orig_pos
    # Adjust starting point based on side we're iterating across
    if side == 'bottom':
        pos = (pos[0], pos[1] + h)
    elif side == 'right':
        pos = (pos[0] + w, pos[1])
    if not (side == 'bottom' or side == 'top' or side == 'left' or side == 'right'):
        raise ValueError('"side" must be "top", "bottom", "left", or "right"')

    # Set up contour variables
    last_contour = None
    current_contour = None

    # Set up loop bools
    testCondition = True
    contour_assigned = False
    while testCondition:
        # Adjust test condition based on side
        if side == 'top' or side == 'bottom':
            testCondition = pos[0] < orig_pos[0] + w
        else:
            testCondition = pos[1] < orig_pos[1] + h

        # Find contour of current position
        for cnt in contours:
            if cv2.pointPolygonTest(cnt, pos, False) < 0:
                continue
            current_contour = cnt
            contour_assigned = True
            break

        # If we found a contour and it's different from our last one, add a new edge
        if (contour_assigned and last_contour is not None):
            current_is_diff = False
            for pt1, pt2 in zip(current_contour, last_contour):
                if not(pt1[0][0] == pt2[0][0] and pt1[0][1] == pt2[0][1]):
                    current_is_diff = True
                    break
            if current_is_diff:
                edge = (get_contour_label(current_contour), get_contour_label(last_contour))
                if edge not in edges:
                    edges.append(edge)
                break

        # Increment position
        if side == 'top' or side == 'bottom':
            pos = (pos[0] + delta, pos[1])
        else:
            pos = (pos[0], pos[1] + delta)

        last_contour = current_contour


def find_doors(img, draw=False):
    """Find the number of doors in a floorplan."""
    doors = []
    w, h = 0, 0
    for door_path in door_paths:
        doors_i, w, h = match_template(img, door_path, DOOR_THRESHOLD, draw)
        for door_i in doors_i:
            doors.append(door_i)
    return doors, w, h


def find_room_contours(img, min_area=MIN_AREA, max_area=MAX_AREA):
    """Find contours of the room."""

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


def get_contour_label(contour):
    return str((hex(sum(contour.flatten()))))


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


def write_svg(path, contours):
    x,y,w,h = cv2.boundingRect(cv2.convexHull(contours))
    c = max(contours, key=cv2.contourArea) # max contour
    f = open(path, 'w+')
    f.write('<svg width="'+str(w)+'" height="'+str(h)+'" xmlns="http://www.w3.org/2000/svg">')
    f.write('<path d="M')

    for i in range(len(c)):
        x, y = c[i][0]
        print(x)
        f.write(str(x)+  ' ' + str(y)+' ')

    f.write('"/>')
    f.write('</svg>')
    f.close()


if __name__ == "__main__":
    pass

