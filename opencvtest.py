import cv2
img = cv2.imread('../1_3.png')

MIN_AREA = 500  # Could be tuned
MAX_AREA

# Make all pixels that aren't pure white into black pixels
ret, img2 = cv2.threshold(img, 254, 255, cv2.THRESH_TOZERO)
# Ensure the image is black and white for finding contours
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


img2, contours, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Array of colors to cycle through
colors = [(0, 255, 0), (0, 255, 255), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
good_contours = []

# Throw out contours that are too small
for cnt in zipcontours:
    if cv2.contourArea(cnt) > MIN_AREA:
        good_contours.append(cnt)

# Draw contours in different colors
for i in range(len(good_contours)):
    cnt = good_contours[i]
    img2 = cv2.drawContours(img, [cnt], -1, colors[i % len(colors)], 1)

# Show image
cv2.imshow('image', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
