import cv2 as cv
import numpy as np

import helper

videoReaderRef = helper.getVideoReader('sample-cut2-raw.yuv', width=3840, height=2160)
videoReaderTest = helper.getVideoReader('raw-ref3.yuv', width=3840, height=2160)

frameCounter = 1
psnrList = []
while True:
    retRef, frameRef = helper.readFrame(videoReaderRef)
    retTest, frameTest = helper.readFrame(videoReaderTest)

    if retRef and retTest:
        # TODO: implement own PSNR measurement function
        psnr = cv.PSNR(frameRef, frameTest)
        # TODO: fix mixed printing with ffmpeg output
        print('Frame {0} PSNR: {1}'.format(frameCounter, round(psnr, 2)))
        psnrList.append(psnr)
        frameCounter += 1
    else:
        # End of either sequence
        break

# TODO: implement SSIM
print('\nMean PSNR value: {0}'.format(round(np.mean(psnrList), 2)))

# TODO: make the program quit after reading all the frames
videoReaderRef.wait()
videoReaderTest.wait()