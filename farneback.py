import sys
import cv2 as cv
import numpy as np
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000, delta_e_cie1976

import helper
import psnr

inputVideoName = '../test-videos/sample-cut-crop-short.mov'
outputVideoName = '../output/sample-cut-crop-short-farneback-0.5-3-30-3-5-1.2-0.mkv'
refVideoName = '../test-videos/room-no-occlusion-crop.mov'

video = helper.openVideo(inputVideoName)

length, width, height, fps = helper.getVideoInfo(video)

# use only avc1 -> H264
# or mp4v -> MPEG4
# with .mov, .avi, .mp4 or .mkv
fourcc = cv.VideoWriter_fourcc(*'ffv1')
writer = cv.VideoWriter(outputVideoName, fourcc, 2 * fps, (width, height))

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
        prevgray = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        gray = cv.cvtColor(frame3, cv.COLOR_BGR2GRAY)

        flow = cv.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 50, 3, 5, 1.2, 0)
        # if not helper.showImage(helper.drawFlow(gray, flow)):
        #     break

        warpedFlow = flow * 0.5

        # TODO: use NaNs or something else instead of 0s to indicate no information
        # newFrame = np.full((height, width, 3), np.nan)
        newFrame = np.zeros((height, width, 3), np.uint8)
        for row in range(height):
            for col in range(width):
                (y, x) = (row, col) + warpedFlow[row, col]
                y = min(int(round(y)), height-1)
                x = min(int(round(x)), width-1)
                newFrame[y, x] = frame3[row, col]

        # # TODO: add blend forward and backward flow, blend only if color difference is not too big
        # # backFlow = cv.calcOpticalFlowFarneback(gray, prevgray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        # # warpedBackFlow = backFlow * 0.5
        # # for row in range(height):
        # #     for col in range(width):
        # #         (y, x) = (row, col) + warpedBackFlow[row, col]
        # #         y = min(int(round(y)), height-1)
        # #         x = min(int(round(x)), width-1)
        # #         if newFrame[y, x].all():
        # #             newFrame[y, x] = np.mean([frame1[row, col], newFrame[y, x]], axis=0)
        # #         else:
        # #             newFrame[y, x] = frame1[row, col]

        # # TODO: iterate only through hole pixel indices
        # # holeInd = np.where(not newFrame.all())
        # # for (row, col, channel) in holeInd:
        for row in range(height):
            for col in range(width):
            # Perform bilinear interpolation, change NaNs to 0s
                # if not np.isnan(newFrame[row,col]).all():
                if newFrame[row,col].all():
                    continue

                d = 1
                points = newFrame[max(row-d,0):min(row+d+1,height-1), max(col-d,0):min(col+d+1,width)]
                points = points.reshape(points.shape[0] * points.shape[1], 3)
                points = points[np.all(points != 0, axis=1)]

                val = np.mean(points, axis=0)
                newFrame[row, col] = val
                    
        # Show interpolated frame
        # if not helper.showImage(newFrame):
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

psnr.calcPSNR(outputVideoName, refVideoName)

video.release()
writer.release()

cv.destroyAllWindows()
