import cv2
import apriltag
import numpy as np

#image = cv2.imread("photo.jpg")

s = 0.01  #apriltag bit length
#CHANGE THESE VALUES TO CA;IBRATION MATRIX YOU GOT FOR YOUR CAM
fx = 752.06947848
fy = 753.05010857
cx = 338.13304823
cy = 272.7434297

cap = cv2.VideoCapture(0)
while True:
    ret, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    options = apriltag.DetectorOptions(families="tag36h11")
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    #print(str(results))

    for r in results:
	# extract the bounding box (x, y)-coordinates for the AprilTag
	# and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (ptB[0], ptB[1])
        ptC = (ptC[0], ptC[1])
        ptD = (ptD[0], ptD[1])
        ptA = (ptA[0], ptA[1])

        ptAi = (int(ptA[0]), int(ptA[1]))
        ptBi = (int(ptB[0]), int(ptB[1]))
        ptCi = (int(ptC[0]), int(ptC[1]))
        ptDi = (int(ptD[0]), int(ptD[1]))
        # draw the bounding box of the AprilTag detection
        cv2.line(image, ptAi, ptBi, (255, 255, 255), 2)
        cv2.line(image, ptBi, ptCi, (255, 255, 255), 2)
        cv2.line(image, ptCi, ptDi, (255, 255, 255), 2)
        cv2.line(image, ptDi, ptAi, (255, 255, 255), 2)
        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(image, (cX, cY), 5, (255, 0, 255), -1)
        # draw the tag family on the image
        tagFamily = r.tag_family.decode("utf-8")
        cv2.putText(image, tagFamily, (ptAi[0], ptAi[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        # print("[INFO] tag family: {}".format(tagFamily))
        # show the output image after AprilTag detection

        # Define known 3D world coordinates of the square corners
        object_points = np.array([
            [-s/2, -s/2, 0],
            [s/2, -s/2, 0],
            [s/2, s/2, 0],
            [-s/2, s/2, 0]
        ], dtype=np.float32)

        # Define corresponding 2D image points (from the camera image)
        image_points = np.array([
            [ptA[0], ptA[1]],  # Top-left corner in image
            [ptB[0], ptB[1]],  # Top-right corner in image
            [ptC[0], ptC[1]],  # Bottom-right corner in image
            [ptD[0], ptD[1]]   # Bottom-left corner in image
        ], dtype=np.float32)


        # Define camera intrinsic matrix K
        K = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1]
        ], dtype=np.float32)

        # Solve for rotation and translation using PnP
        success, rvec, tvec = cv2.solvePnP(object_points, image_points, K, None)

        # Convert rotation vector to rotation matrix
        R, _ = cv2.Rodrigues(rvec)

        R_camera = R.T
        t_camera = -R.T @ tvec

        print(R_camera)
        print(t_camera)





    cv2.imshow("Image", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    # [Detection(
    #     tag_family=b'tag36h11', 
    #     tag_id=0, 
    #     hamming=0, 
    #     goodness=0.0, 
    #     decision_margin=46.07822799682617, 
    #     homography=array(
    #         [[ 7.57930545e-01, -8.54602128e-02, -2.86523102e+00],
    #         [ 6.68563226e-02,  6.02431931e-01, -3.14705222e+00],
    #         [ 1.88753793e-04, -3.35805113e-04, -9.91045967e-03]]), 
    #     center=array([289.11181885, 317.54856199]), 
    #     corners=array(
    #         [[362.34286499, 390.88198853],
    #         [215.41249084, 392.35742187],
    #         [218.02220154, 246.35955811],
    #         [355.40155029, 250.260849  ]]))]

