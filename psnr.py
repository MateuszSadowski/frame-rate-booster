import cv2 as cv
import numpy as np

capRef = cv.VideoCapture('sample.mov')
capTest = cv.VideoCapture('output-ref.mp4')

if not capRef.isOpened():
    print('Error opening reference video file.')
    sys.exit(2)
elif not capTest.isOpened():
    print('Error opening test video file.')
    sys.exit(2)

frameCounter = 0
psnrList = []
while(capRef.isOpened() and capTest.isOpened()):
    retRef, frameRef = capRef.read()
    retTest, frameTest = capTest.read()

    if retRef and retTest:
        # TODO: implement own PSNR measurement function
        psnr = cv.PSNR(frameRef, frameTest)
        print('Frame {0} PSNR: {1}'.format(frameCounter, psnr))
        psnrList.append(psnr)
        frameCounter += 1
    else:
        # End of either sequence
        break

# TODO: implement SSIM
print('\nMean PSNR value: {0}'.format(np.mean(psnrList)))

capRef.release()
capTest.release()

cv.destroyAllWindows()