import sys
import cv2 as cv
import numpy as np

cap = cv.VideoCapture('sample.mov')

if not cap.isOpened():
    print('Error opening video file.')
    sys.exit(2)

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')

if int(major_ver)  < 3 :
    fps = cap.get(cv.cv.CV_CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
else :
    fps = cap.get(cv.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

ret, frame = cap.read()
size = frame.shape

writer = cv.VideoWriter('output.avi', cv.VideoWriter_fourcc('M','J','P','G'), 2 * fps, (size[1], size[0]))

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        # Show next frame after specified interval or press q to exit
        # cv.imshow('Frame', frame)
        # if cv.waitKey(25) & 0xFF == ord('q'):
        #     break

        # Write frames to new video file
        writer.write(frame)
        writer.write(np.zeros((size[0], size[1], 3), np.uint8))
    else:
        # End of sequence
        break

cap.release()
writer.release()

cv.destroyAllWindows()
