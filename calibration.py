import cv2
import numpy as np
import glob

collumns = 11
rows = 8
square_size = 0.01  # 1cm

# Checkerboard size (number of inner corners)
CHECKERBOARD = (collumns-1, rows-1)  # 9x6 inner corners

# Prepare object points in meters
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= square_size  # Convert to meters

# Lists to store object points and image points
objpoints = []  # 3D world points in meters
imgpoints = []  # 2D image points in pixels

# Load all checkerboard images
images = glob.glob("calibration_images/*.jpg")  # Change this to your image folder

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Draw detected corners
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)
        cv2.imshow("Checkerboard", img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Camera calibration (intrinsic matrix K will still be in pixels)
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Print results
print("Camera Intrinsic Matrix (K) in pixels:\n", K)
print("Distortion Coefficients:\n", dist)

# Save calibration results
np.save("intrinsics.npy", K)
np.save("distortion.npy", dist)
