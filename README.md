# apriltag_detector

## Requirements
```
python3 -m venv *venv-name*
source *venv-name*/bin/activate
pip install -r requirements
```

## Calibration

Calibration scripts uses images from
**./calibration_images/** folder in jpg format, but you can change it by changing **images_path** variable in the **calibration.py** file.

**Run the calibration:**
```
python3 calibration.py
```
**You'll get the result in form of**
```
Camera Intrinsic Matrix (K):
 [[ fx           0.           cx        ]
 [  0.           fy           cy        ]
 [  0.           0.           1.        ]]
Distortion Coefficients:
 [[ 0.11182688 -0.46921992  0.00868996  0.00395888  0.2290846 ]]
 ```
**Take the coefficients fx, fy, cx, cy from this matrix**
**and put it into the head of main.py file**

```
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
```
**And put here**

**Run the main.py:**
```
python3 main.py
```
**It will print the output like**
```
[[ 0.93304838 -0.14627087 -0.3286724 ]
 [ 0.09306069  0.98064944 -0.17223934]
 [ 0.347506    0.13012116  0.92860544]]
[[ 0.00705928]
 [ 0.00460102]
 [-0.0546133 ]]
 ```

**Which is Camera Transformation matrix (relative to tag) and Camera Position (relative to tag)**