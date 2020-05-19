import sys
import cv2 as cv
import numpy as np

def openVideo(name):
    cap = cv.VideoCapture(name)

    if not cap.isOpened():
        print('Error opening video file ' + name)
        sys.exit(2)

    return cap

def getVideoInfo(video):
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')

    if int(major_ver)  < 3 :
        fps = video.get(cv.cv.CV_CAP_PROP_FPS)
        length = int(video.get(cv.cv.CV_CAP_PROP_FRAME_COUNT))
        width = video.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
        height = video.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)
    else :
        fps = video.get(cv.CAP_PROP_FPS)
        length = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        width = video.get(cv.CAP_PROP_FRAME_WIDTH)
        height = video.get(cv.CAP_PROP_FRAME_HEIGHT)

    print('Frames per second: {0}'.format(fps))

    return length, int(width), int(height), fps

def readFrame(video):
    ret, frame = video.read()
    if ret:
        return frame
    else:
        # End of sequence
        print('End of video file')
        sys.exit(0)

def drawFlow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    cv.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (_x2, _y2) in lines:
        cv.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

def showImage(img, timeout=0, label="Frame"):
    cv.imshow('Frame', img)
    if cv.waitKey(timeout) & 0xFF == ord('q'):
        return False
    return True