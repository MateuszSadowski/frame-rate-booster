import sys
import cv2 as cv
import numpy as np
import ffmpeg

def openVideoOpenCV(name):
    cap = cv.VideoCapture(name)

    if not cap.isOpened():
        print('Error opening video file ' + name)
        sys.exit(2)

    return cap

def getVideoReader(filename, width=-1, height=-1):
    if width != -1 and height != -1:
        videoReader = (
            ffmpeg
            .input(filename, s='{}x{}'.format(width, height))
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run_async(pipe_stdout=True)
        )
    else:
        videoReader = (
            ffmpeg
            .input(filename)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run_async(pipe_stdout=True)
        )

    return videoReader

def getVideoWriter(filename, codec='rawvideo', pixFormat='yuv420p', width=3840, height=2160):
    videoWriter = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
        .output(filename, format=codec, pix_fmt=pixFormat)
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    return videoWriter

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

def readFrame(videoReader, width=3840, height=2160):
    inBytes = videoReader.stdout.read(width * height * 3)
    if not inBytes:
        print('Error: could not read frame.')
        return False, None
    else:
        frame = (
            np
            .frombuffer(inBytes, np.uint8)
            .reshape([height, width, 3])
        )
    
    return True, frame

def writeFrame(videoWriter, frame):
    videoWriter.stdin.write(
        frame
        .astype(np.uint8)
        .tobytes()
    )

def showFrame(frame, timeOut=0):
    cv.imshow('Frame', frame)
    if cv.waitKey(timeOut) & 0xFF == ord('q'):
        return False    # user wants to quit
    return True

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