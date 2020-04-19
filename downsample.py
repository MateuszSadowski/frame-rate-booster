import cv2 as cv

import helper

video = helper.openVideo('sample.mov')

length, width, height, fps = helper.getVideoInfo(video)

# use only avc1 -> H264
# or mp4v -> MPEG4
# with .mov, .avi, .mp4 or .mkv
fourcc = cv.VideoWriter_fourcc(*'avc1')
writer = cv.VideoWriter('output-downsampled.mp4', fourcc, fps / 2, (width, height))

frameCounter = 1
while(video.isOpened()):
    ret, frame = video.read()

    if ret:
        if frameCounter % 2:
            # Discard every second frame
            print('Writing frame {0}/{1}'.format(frameCounter, length), end='\r')
            writer.write(frame)
        frameCounter += 1
    else:
        # End of either sequence
        break

print('\nSuccess')

video.release()
writer.release()

cv.destroyAllWindows()