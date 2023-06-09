import numpy as np
import cv2

# # Read image
# img = cv2.imread("imgs/box-1.jpeg")

# # Gaussian blur
# blurred = cv2.GaussianBlur(img, (5, 5), 0)
# cv2.imshow("blurred", blurred)
# cv2.waitKey(0)

# # Convert to graysscale
# gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
# cv2.imshow("grayscale", gray)
# cv2.waitKey(0)

# # !!! DILATION !!!

# # Autocalculate the thresholding level
# threshold = cv2.adaptiveThreshold(
#     gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
# )

# # Threshold
# retval, bin = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
# cv2.imshow("binary", bin)
# cv2.waitKey(0)

# # Find contours
# contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# # Sort out the biggest contour (biggest area)
# max_area = 0
# max_index = -1
# index = -1
# for i in contours:
#     area = cv2.contourArea(i)
#     index = index + 1
#     if area > max_area:
#         max_area = area
#         max_index = index

# # Draw the raw contours
# cv2.drawContours(img, contours, max_index, (0, 255, 0), 3)
# # cv2.imwrite("box-1-biggest-contour.png", img)

# # Draw a rotated rectangle of the minimum area enclosing our box (red)
# cnt = contours[max_index]
# rect = cv2.minAreaRect(cnt)
# box = cv2.boxPoints(rect)
# box = np.int0(box)
# img = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

# # Show original picture with contour
# cv2.namedWindow("image", cv2.WINDOW_NORMAL)
# cv2.imshow("image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# def get_contours_image(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (7, 7), 0.5)
#     edge = cv2.Canny(blur, 0, 50, 3)

#     contours, hierarchy = cv2.findContours(
#         edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#     )

#     for contour, hier in zip(contours, hierarchy):
#         (x, y, w, h) = cv2.boundingRect(contour)
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.putText(
#             frame,
#             ("width = {}, height = {}".format(w, h)),
#             (x + 30, y + 30),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             1,
#             (0, 255, 0),
#             2,
#             cv2.LINE_AA,
#         )
#     return frame


def get_contours_image(img):
    # Gaussian blur
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    # Convert to graysscale
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    # Autocalculate the thresholding level
    threshold = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    # Threshold
    retval, bin = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    # Find contours
    contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Return if no contours found
    if len(contours) < 1:
        return img
    # Sort out the biggest contour (biggest area)
    max_area = 0
    max_index = -1
    index = -1
    for i in contours:
        area = cv2.contourArea(i)
        index = index + 1
        if area > max_area:
            max_area = area
            max_index = index
    # Draw the raw contours
    cv2.drawContours(img, contours, max_index, (0, 255, 0), 3)
    # Draw a rotated rectangle of the minimum area enclosing our box (red)
    cnt = contours[max_index]
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    img = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    return img
