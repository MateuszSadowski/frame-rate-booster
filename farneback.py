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
writer = cv.VideoWriter('../output/room-no-occlusion-crop-farneback-6.mkv', fourcc, 2 * fps, (width, height))

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

        warpedFlow = flow * 0.5
        # newFrame = np.full((height, width, 3), np.nan)
        newFrame = np.zeros((height, width, 3), np.uint8)
        for row in range(height):
            for col in range(width):
                (y, x) = (row, col) + warpedFlow[row, col]
                y = min(int(round(y)), height-1)
                x = min(int(round(x)), width-1)
                newFrame[y, x] = frame3[row, col]

        # backFlow = cv.calcOpticalFlowFarneback(gray, prevgray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        # warpedBackFlow = backFlow * 0.5
        # for row in range(height):
        #     for col in range(width):
        #         (y, x) = (row, col) + warpedBackFlow[row, col]
        #         y = min(int(round(y)), height-1)
        #         x = min(int(round(x)), width-1)
        #         if newFrame[y, x].all():
        #             newFrame[y, x] = np.mean([frame1[row, col], newFrame[y, x]], axis=0)
        #         else:
        #             newFrame[y, x] = frame1[row, col]

        # holeInd = np.where(not newFrame.all())

        # for (row, col, channel) in holeInd:
        for row in range(height):
            for col in range(width):
            # Perform bilinear interpolation, change NaNs to 0s
                # if not np.isnan(newFrame[row,col]).all():
                if newFrame[row,col].all():
                    continue

                # p00 = np.full(3, 127, np.uint8)
                # p01 = np.full(3, 127, np.uint8)
                # p10 = np.full(3, 127, np.uint8)
                # p11 = np.full(3, 127, np.uint8)
                # if row-1 >= 0 and col-1 >= 0 and not np.isnan(newFrame[row-1, col-1]).any():
                d = 1
                points = newFrame[max(row-d,0):min(row+d+1,height-1), max(col-d,0):min(col+d+1,width)]
                points = points.reshape(points.shape[0] * points.shape[1], 3)
                points = points[np.all(points != 0, axis=1)]
                # if row-d >= 0 and col-d >= 0 and newFrame[row-d,col-d].all():
                #     p00 = newFrame[row-d, col-d]
                # # if row+d <= height-d and col-d >= 0 and not np.isnan(newFrame[row+d, col-d]).any():
                # if row+d <= height-d and col-d >= 0 and newFrame[row+d,col-d].all():
                #     p01 = newFrame[row+d, col-d]
                # # if row-d >= 0 and col+d <= width-d and not np.isnan(newFrame[row-d, col+d]).any():
                # if row-d >= 0 and col+d <= width-d and newFrame[row-d,col+d].all():
                #     p10 = newFrame[row-d, col+d]
                # # if row+d <= height-d and col+d <= width-d and not np.isnan(newFrame[row+d, col+d]).any():
                # if row+d <= height-d and col+d <= width-d and newFrame[row+d,col+d].all():
                #     p11 = newFrame[row+d, col+d]

                # points = [(row-d, col-d, p00), (row+d, col-d, p01), (row-d, col+d, p10), (row+d, col+d, p11)]
                # val = helper.bilinear_interpolation(row, col, points)
                # newFrame[row, col] = val
                # val = np.mean([p00, p01, p10, p11], axis=0)

                val = np.mean(points, axis=0)
                newFrame[row, col] = val
                    
        # Show next frame after specified interval or press q to exit
        cv.imshow('Frame', newFrame)
        if cv.waitKey(0) & 0xFF == ord('q'):
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
