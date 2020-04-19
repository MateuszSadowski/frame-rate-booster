import cv2 as cv
import numpy as np

import helper

videoRef = helper.openVideo('sample.mov')
videoTest = helper.openVideo('output-ref.mp4')

frameCounter = 1
psnrList = []
while(videoRef.isOpened() and videoTest.isOpened()):
    retRef, frameRef = videoRef.read()
    retTest, frameTest = videoTest.read()

    if retRef and retTest:
        # TODO: implement own PSNR measurement function
        psnr = cv.PSNR(frameRef, frameTest)
        print('Frame {0} PSNR: {1}'.format(frameCounter, round(psnr, 2)))
        psnrList.append(psnr)
        frameCounter += 1
    else:
        # End of either sequence
        break

# TODO: implement SSIM
print('\nMean PSNR value: {0}'.format(round(np.mean(psnrList), 2)))

videoRef.release()
videoTest.release()

cv.destroyAllWindows()