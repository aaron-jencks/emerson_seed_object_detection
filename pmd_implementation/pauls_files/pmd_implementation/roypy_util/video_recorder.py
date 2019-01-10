import numpy as np
import cv2
import argparse


# Sets up the arguments
parser = argparse.ArgumentParser(description="Creates a video from into the given output directory using the given device ID, use space to toggle recording, and 'k' to take a snapshot, hit esc or 'q' to quit")
parser.add_argument('-o', '--output', help='The output path that the video will be created at, defaults to ./output.avi.', type=str, default='./output.avi')
parser.add_argument('device', help='The device ID /dev/videoN where N is the ID', type=int)
args = parser.parse_args()

cap = cv2.VideoCapture(args.device)

# either *'XVID' or ('X', 'V', 'I', 'D') will work the same way
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# output path, video config, fps, screen resolution, isColor
out = cv2.VideoWriter(args.output, fourcc, int(cap.get(5)), (640, 480)) #int(cap.get(3)), int(cap.get(4))))

# Variables for video operation
isRecording = False
snapshot = False

while cap.isOpened():
	ret, frame = cap.read()
	if ret:
		if isRecording or snapshot:
			out.write(frame)
			if snapshot:
				snapshot = False

		cv2.imshow('frame', frame)

		k = cv2.waitKey(1) & 0xFF
		if k == ord('q') or k == 27:
			break
		elif k == 32:
			isRecording = not isRecording
			print('Recording Started' if isRecording else 'Recording Stopped')
		elif k == 107:
			snapshot = True
			print('Collecting snapshot' if not isRecording else "Can't take a snapshot while recording silly, I'm already taking in frames")
	else:
		break

cap.release()
out.release()
cv2.destroyAllWindows()

