import cv2
import numpy as np
import glob

# Chessboard size (number of inner corners per row and column)
CHECKERBOARD = (10, 7)

# Prepare object points (3D world coordinates)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Lists to store object points and image points
objpoints = []  # 3D world points
imgpoints = []  # 2D image points

# Load all checkerboard images
images = glob.glob("calibration_images/*.jpg")  # Change path as needed

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)
        cv2.imshow("Checkerboard", img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Camera calibration
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Print the camera intrinsic matrix
print("Camera Intrinsic Matrix (K):\n", K)
print("Distortion Coefficients:\n", dist)

# Save calibration results
np.save("intrinsics.npy", K)
np.save("distortion.npy", dist)