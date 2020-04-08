import cv2 as cv

cap = cv.VideoCapture('sample.mov')

if not cap.isOpened():
    print('Error opening video file.')

frameCounter = 0
while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        cv.imshow('Frame', frame)
        # Show next frame after specified interval or press q to exit
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
        frameCounter += 1
    else:
        # End of sequence
        break

cap.release()

cv.detroyAllWindows()
