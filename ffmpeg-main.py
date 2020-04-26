import sys
import cv2 as cv
import numpy as np
import ffmpeg

import helper

inFilename = "sample.mov"
outFilename = "ffmpeg-output.yuv"
framesToProcess = 50

videoReader = helper.getVideoReader(inFilename)
videoWriter = helper.getVideoWriter(outFilename)

while True:
    if framesToProcess <= 0:
        break
    framesToProcess -= 1
    
    frame1 = helper.readFrame(videoReader)
    frame2 = helper.readFrame(videoReader)
    prevgray = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    gray = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    cv.imshow('flow', helper.drawFlow(gray, flow))
    if cv.waitKey(25) & 0xFF == ord('q'):
        break
    # helper.writeFrame(videoWriter, frame)

videoWriter.stdin.close()
videoReader.wait()
videoWriter.wait()