import sys
import cv2 as cv
import numpy as np

import helper

video = helper.openVideo('sample.mov')

length, width, height, fps = helper.getVideoInfo(video)

# use only avc1 -> H264
# or mp4v -> MPEG4
# with .mov, .avi, .mp4 or .mkv
fourcc = cv.VideoWriter_fourcc(*'avc1')
writer = cv.VideoWriter('output.mp4', fourcc, 2 * fps, (width, height))

ret1, frame1 = video.read()
if not ret1:
    # End of sequence
    print('Empty video file')
    sys.exit(2)

frameCounter = 1
while(video.isOpened()):
    print('Processing frame {0}/{1}'.format(frameCounter, length), end='\r')
    ret3, frame3 = video.read()
    if ret3:
        # Show next frame after specified interval or press q to exit
        # cv.imshow('Frame', frame)
        # if cv.waitKey(25) & 0xFF == ord('q'):
        #     break

        # Add interpolated frame
        # frame2 = cv.addWeighted(frame1, 0.5, frame3, 0.5, 0.0)
        prevgray = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        gray = cv.cvtColor(frame3, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        cv.imshow('flow', helper.drawFlow(gray, flow))
        # cv.waitKey(0)
        # cv.imshow('Frame', frame3)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break

        # Write frames to new video file
        # writer.write(frame1)
        # writer.write(frame2)

        frame1 = frame3

        frameCounter += 1
    else:
        # End of sequence
        # writer.write(frame1)
        break

print('\nSuccess')

video.release()
writer.release()

cv.destroyAllWindows()
