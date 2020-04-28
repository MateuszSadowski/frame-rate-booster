import sys
import cv2 as cv
import numpy as np

import helper

video = helper.openVideo('output-cut-crop-downsampled.mkv')

length, width, height, fps = helper.getVideoInfo(video)

# use only avc1 -> H264
# or mp4v -> MPEG4
# with .mov, .avi, .mp4 or .mkv
fourcc = cv.VideoWriter_fourcc(*'ffv1')
writer = cv.VideoWriter('output-farneback-crop.mkv', fourcc, 2 * fps, (width, height))

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
        # cv.imshow('flow', helper.drawFlow(gray, flow))
        warpedFlow = flow * 0.5
        newFrame = np.zeros((height, width, 3), np.uint8)
        for row in range(height):
            for col in range(width):
                pixelVal = frame1[row, col]
                (y, x) = (row, col) + warpedFlow[row, col]
                x1 = min(int(round(x + 0.5)), width-1)
                x2 = min(int(max(round(x - 0.5), 0)), width-1)
                y1 = min(int(round(y + 0.5)), height-1)
                y2 = min(int(max(round(y - 0.5), 0)), height-1)
                y = min(int(round(y)), height-1)
                x = min(int(round(x)), width-1)
                newFrame[y, x] = pixelVal
                if x1 < width:
                    newFrame[y, x1] = pixelVal
                newFrame[y, x2] = pixelVal
                if y1 < height:
                    newFrame[y1, x] = pixelVal
                newFrame[y2, x] = pixelVal

        # cv.imshow('Frame', newFrame)
        # cv.waitKey(0)
        # if cv.waitKey(25) & 0xFF == ord('q'):
        #     break

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
