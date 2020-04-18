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

ret1, frame1 = cap.read()
if ret1:
    frameSize = frame1.shape
else:
    # End of sequence
    print('Empty video file.')
    sys.exit(2)

# use only avc1 -> h264
# or mp4v -> MPEG4
# with .mov, .avi, .mp4 or .mkv
fourcc = cv.VideoWriter_fourcc(*'avc1')
writer = cv.VideoWriter('output.mp4', fourcc, 2 * fps, (frameSize[1], frameSize[0]))

while(cap.isOpened()):
    ret3, frame3 = cap.read()
    if ret3:
        # Show next frame after specified interval or press q to exit
        # cv.imshow('Frame', frame)
        # if cv.waitKey(25) & 0xFF == ord('q'):
        #     break

        # Add interpolated frame
        frame2 = cv.addWeighted(frame1, 0.5, frame3, 0.5, 0.0)
        # cv.imshow('Frame', frame3)
        # if cv.waitKey(0) & 0xFF == ord('q'):
        #     break

        # Write frames to new video file
        writer.write(frame1)
        writer.write(frame2)

        frame1 = frame3
    else:
        # End of sequence
        writer.write(frame1)
        break

cap.release()
writer.release()

cv.destroyAllWindows()
