import sys
import cv2 as cv
import numpy as np
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000, delta_e_cie1976

import helper
import rgb2lab

video = helper.openVideo('../downsampled/room-no-occlusion-crop-downsampled.mkv')

length, width, height, fps = helper.getVideoInfo(video)

# use only avc1 -> H264
# or mp4v -> MPEG4
# with .mov, .avi, .mp4 or .mkv
fourcc = cv.VideoWriter_fourcc(*'ffv1')
writer = cv.VideoWriter('../output/room-no-occlusion-crop-farneback-3.mkv', fourcc, 2 * fps, (width, height))

def testColorDiff(newVal, currVal, refVal):
    # newValLab = rgb2lab.rgb2lab(newVal)
    # currValLab = rgb2lab.rgb2lab(currVal)
    # refValLab = rgb2lab.rgb2lab(refVal)

    newValLab = LabColor(newVal[0], newVal[1], newVal[2])
    currValLab = LabColor(currVal[0], currVal[1], currVal[2])
    refValLab = LabColor(refVal[0], refVal[1], refVal[2])

    currDiff = delta_e_cie1976(currValLab, refValLab)
    newDiff = delta_e_cie1976(newValLab, refValLab)

    if newDiff < currDiff:
        return newVal
    else:
        return currVal

# lab1 = rgb2lab.rgb2lab([0.1, 0.2, 0.3])
# lab2 = rgb2lab.rgb2lab([0.1, 3, 0.3])
# labLab1 = LabColor(lab1[0], lab1[1], lab1[2])
# labLab2 = LabColor(lab2[0], lab2[1], lab2[2])
# diff = delta_e_cie2000(labLab1, labLab2)
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
        # frame2 = cv.addWeighted(frame1, 0.5, frame3, 0.5, 0.0)
        prevgray = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        gray = cv.cvtColor(frame3, cv.COLOR_BGR2GRAY)
        # if cv.waitKey(25) & 0xFF == ord('q'):
        #     break
        flow = cv.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        # cv.imshow('flow', helper.drawFlow(gray, flow))
        # if cv.waitKey(0) & 0xFF == ord('q'):
        #     break

        prevlab = cv.cvtColor(frame1, cv.COLOR_BGR2LAB)
        lab = cv.cvtColor(frame3, cv.COLOR_BGR2LAB)

        warpedFlow = flow * 0.5
        newFrame = np.zeros((height, width, 3), np.uint8)
        for row in range(height):
            for col in range(width):
                # print("{0}, {1}".format(row,col))
                pixelVal = frame1[row, col]
                pixelValLab = frame1[row, col]
                (y, x) = (row, col) + warpedFlow[row, col]
                x1 = min(int(round(x + 0.5)), width-1)
                x2 = min(int(max(round(x - 0.5), 0)), width-1)
                y1 = min(int(round(y + 0.5)), height-1)
                y2 = min(int(max(round(y - 0.5), 0)), height-1)
                y = min(int(round(y)), height-1)
                x = min(int(round(x)), width-1)
                newFrame[y, x] = testColorDiff(pixelValLab, newFrame[y, x], lab[y, x])
                if x1 < width:
                    newFrame[y, x1] = testColorDiff(pixelValLab, newFrame[y, x1], lab[y, x1])
                    newFrame[y2, x1] = testColorDiff(pixelValLab, newFrame[y2, x1], lab[y2, x1])
                    if y1 < height:
                        newFrame[y1, x1] = testColorDiff(pixelValLab, newFrame[y1, x1], lab[y1, x1])
                newFrame[y, x2] = testColorDiff(pixelValLab, newFrame[y, x2], lab[y, x2])
                if y1 < height:
                    newFrame[y1, x] = testColorDiff(pixelValLab, newFrame[y1, x], lab[y1, x])
                    newFrame[y1, x2] = testColorDiff(pixelValLab, newFrame[y1, x2], lab[y1, x2])
                newFrame[y2, x] = testColorDiff(pixelValLab, newFrame[y2, x], lab[y2, x])
                newFrame[y2, x2] = testColorDiff(pixelValLab, newFrame[y2, x2], lab[y2, x2])

        newFrame = cv.cvtColor(newFrame, cv.COLOR_LAB2RGB)

        # Show next frame after specified interval or press q to exit
        # cv.imshow('Frame', newFrame)
        # if cv.waitKey(0) & 0xFF == ord('q'):
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
