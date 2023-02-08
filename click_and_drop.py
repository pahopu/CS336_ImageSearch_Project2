import cv2

refPt = []
cropping = False


def cropper(path):
    image = cv2.imread(path)
    clone = image.copy()
    cv2.namedWindow("image")

    def helper(event, x, y, flags, param):

        # grab references to the global variables
        global refPt, cropping

        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt.append((x, y))
            cropping = False
            # draw a rectangle around the region of interest
            cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", image)

    cv2.setMouseCallback("image", helper)

    cv2.imshow("image", image)
    cv2.waitKey(0)

    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        print(roi.shape)
        cv2.imshow("ROI", roi)
        cv2.imwrite("query.jpg", roi)
        cv2.waitKey(0)

    cv2.destroyAllWindows()