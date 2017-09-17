import cv2

default_filepath = '../1_3.png'
MIN_AREA = 500  # Could be tuned
MAX_AREA = 20000  # Could be tuned

def find_room_contours(min_area=MIN_AREA, max_area=MAX_AREA, path=default_filepath):
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
