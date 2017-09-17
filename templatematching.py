import cv2
import numpy as np

default_filepath = '../1_3.png'
template_path = 'door_down.png'

def match_template(img_path, template_path, threshold=8*10**5):
    img_color = cv2.imread(img_path)
    img = cv2.imread(img_path, 0)
    temp = cv2.imread(template_path, 0)

    w, h = temp.shape[::-1]

    result = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF)
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_color, pt, (pt[0]+w, pt[1]+h), (255, 255, 0), 2)

    # Show image
    cv2.imshow('image', img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    match_template(default_filepath, template_path)
