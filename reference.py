import cv2 as cv

cap = cv.VideoCapture('sample.mov')

if not cap.isOpened():
    print('Error opening reference video file.')
    sys.exit(2)

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')

if int(major_ver)  < 3 :
    fps = cap.get(cv.cv.CV_CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
else :
    fps = cap.get(cv.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

ret, frame = cap.read()
if ret:
    frameSize = frame.shape
else:
    # End of sequence
    print('Empty video file.')
    sys.exit(2)

# use only avc1 -> h264
# or mp4v -> MPEG4
# with .mov, .avi, .mp4 or .mkv
fourcc = cv.VideoWriter_fourcc(*'avc1')
writer = cv.VideoWriter('output-ref.mp4', fourcc, fps, (frameSize[1], frameSize[0]))

writer.write(frame)

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        writer.write(frame)
    else:
        # End of either sequence
        break

cap.release()

cv.destroyAllWindows()