import cv2 as cv

import helper

videoReader = helper.getVideoReader('sample-cut2-raw.yuv', width=3840, height=2160)
videoWriter= helper.getVideoWriter('raw-ref4.yuv')

# For print outs
# TODO: get this from ffmpeg
# video = helper.openVideoOpenCV('sample-cut.mov')
# length, width, height, fps = helper.getVideoInfo(video)

frameCounter = 1
while True:
    ret, frame = helper.readFrame(videoReader)

    if ret:
        # print('Writing frame {0}/{1}'.format(frameCounter, length), end='\r')
        # helper.showFrame(frame)
        helper.writeFrame(videoWriter, frame)
        frameCounter += 1
    else:
        # End of sequence
        break

print('\nSuccess')

videoWriter.stdin.close()
videoReader.wait()
videoWriter.wait()