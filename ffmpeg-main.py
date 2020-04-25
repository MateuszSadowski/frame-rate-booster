import sys
import cv2 as cv
import numpy as np
import ffmpeg

import helper

in_filename = "sample.mov"
out_filename = "ffmpeg-output.yuv"
width = 3840
height = 2160
framesToProcess = 50

process1 = (
    ffmpeg
    .input(in_filename)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .run_async(pipe_stdout=True)
)

process2 = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
    .output(out_filename, format='rawvideo', pix_fmt='yuv420p')
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

while True:
    if framesToProcess <= 0:
        break
    framesToProcess -= 1
    
    in_bytes = process1.stdout.read(width * height * 3)
    if not in_bytes:
        break
    in_frame1 = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([height, width, 3])
    )
    in_bytes = process1.stdout.read(width * height * 3)
    if not in_bytes:
        break
    in_frame2 = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([height, width, 3])
    )
    prevgray = cv.cvtColor(in_frame1, cv.COLOR_BGR2GRAY)
    gray = cv.cvtColor(in_frame2, cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    cv.imshow('flow', helper.drawFlow(gray, flow))
    # cv.waitKey(0)
    # cv.imshow('Frame', frame3)
    if cv.waitKey(25) & 0xFF == ord('q'):
        break
    # cv.imshow('Frame', in_frame)
    # if cv.waitKey(0) & 0xFF == ord('q'):
    #      break
    # out_frame = in_frame * 0.3
    # process2.stdin.write(
    #     out_frame
    #     .astype(np.uint8)
    #     .tobytes()
    # )

process2.stdin.close()
process1.wait()
process2.wait()