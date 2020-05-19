import sys
import cv2 as cv
import numpy as np

import helper

video = helper.openVideo('../downsampled/room-no-occlusion-crop-downsampled.mkv')

length, width, height, fps = helper.getVideoInfo(video)

# use only avc1 -> H264
# or mp4v -> MPEG4
# with .mov, .avi, .mp4 or .mkv
fourcc = cv.VideoWriter_fourcc(*'ffv1')
writer = cv.VideoWriter('../output/room-no-occlusion-crop-blend.mkv', fourcc, 2 * fps, (width, height))

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
        # Add interpolated frame
        newFrame = cv.addWeighted(frame1, 0.5, frame3, 0.5, 0.0)
                    
        # Show interpolated frame
        if not helper.showImage(newFrame):
            break

        # Write frames to new video file
        writer.write(frame1)
        writer.write(newFrame)

        frame1 = frame3

        frameCounter += 1
    else:
        # End of sequence
        writer.write(frame1)
        break

print('\nSuccess')

video.release()
writer.release()

cv.destroyAllWindows()
