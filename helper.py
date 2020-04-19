import cv2 as cv

def openVideo(name):
    cap = cv.VideoCapture(name)

    if not cap.isOpened():
        print('Error opening reference video file')
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