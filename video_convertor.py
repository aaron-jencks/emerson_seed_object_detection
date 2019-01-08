import argparse
import cv2
import numpy as np

# Sets up the argument parser
parser = argparse.ArgumentParser("Converts a .avi file into a series of jpg images all named starting from 1 up to N where N is the number of frames in the video")
parser.add_argument('--output_path', help="The output directory to save the images to", type=str, default='.')
parser.add_argument('--output_filename', help="The prefix to the images, '_1.jpg' will be appended to the first, then '_2.jpg', etc...", type=str, default='img')
parser.add_argument('--start_num', help="The starting number for counting (the '_N.jpg' part).", type=int, default=1)
parser.add_argument('input_file', nargs='+', help="The file to read the frames from (must be avi)", type=str)
args = parser.parse_args()

fr = args.start_num

for filename in args.input_file:
	print('Converting ' + filename)
	input = cv2.VideoCapture(filename)

	# simulates a do-while loop, loops while the reader succeeds in reading the next frame, the first read has to be out here to work
	ret, frame = input.read()

	while ret:
		output_path =  args.output_path + "/" + args.output_filename + "_" + str(fr) + ".jpg"

		print("Saving " + output_path)
		cv2.imwrite(output_path, frame)
		ret, frame = input.read()
		fr += 1
