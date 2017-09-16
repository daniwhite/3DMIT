import cv2
img = cv2.imread('../1_3.png')

MIN_AREA = 500

ret,img2 = cv2.threshold(img,254,255,cv2.THRESH_TOZERO)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

img2, contours, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(len(contours))
colors = [(0, 255, 0), (0, 255, 255), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
good_contours = []
for i in contours:
    if cv2.contourArea(i) > MIN_AREA:
        good_contours.append(i)
for i in range(len(good_contours)):
    cnt = good_contours[i]
    img2 = cv2.drawContours(img, [cnt], -1, colors[i % len(colors)], 1)

cv2.imshow('image', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
