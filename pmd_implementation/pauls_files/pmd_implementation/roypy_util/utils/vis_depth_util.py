import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

#np.set_printoptions(threshold=np.nan)

def apply_depth_to_boxes(image, boxes, scores, depth_frame):
	"""Draws a caption label in the center of the
	bounding box for the depth of the object."""

	# Converts the image into a PIL image
	image_pil = Image.fromarray(np.uint8(image)).convert('RGB')

	# Converts the depth_frame into an image
	depth_image = depth_frame
	#depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
	depth_image = cv2.convertScaleAbs(depth_image)

	# Drawing functions
	draw = ImageDraw.Draw(image_pil)
	im_width, im_height = image_pil.size

	# Sets the font
	try:
		font = ImageFont.truetype('arial.ttf', 8)
	except IOError:
		font = ImageFont.load_default()

	"""
	for y in range(im_height):
		for x in range(im_width):
			if depth_image[y, x] > 1:
				draw.point((x, y), 'blue')
	"""

	for i in range(len(boxes)):

		if scores is None or scores[i] > 0.7:
			# Gets bounding information
			(ymin, xmin, ymax, xmax) = tuple(boxes[i].tolist())
			(left, right, top, bottom) = (int(xmin * im_width), int(xmax * im_width), 
				int(ymin * im_height), int(ymax * im_height))

			# Scales the depth data into range
			region_of_interest = depth_image[top:bottom, left:right].astype(float)

			# print(region_of_interest)
			
			for y in range(top, bottom):
				for x in range(left, right):
					if depth_image[y, x] > 1:
						draw.point((x, y), 'blue') 
			

			# Find the min, max, and mean distances
			min = region_of_interest.min()
			max = region_of_interest.max()
			m, _, _, _ = cv2.mean(region_of_interest)
			
			print("Data: (min: " + str(round(min, 4)) + ", mean: " + str(round(m, 4)) + ", max: " + str(round(max, 4)) + ")")

			# Formats the display string
			text_bottom = bottom
			display_str_list = list([
				'Distance:',
				'min: ' + str(round(min, 4)) + ' m',
				'mean: ' + str(round(m, 4)) + ' m',
				'max: ' + str(round(max, 4)) + ' m'])
			
			# Reverse list and print from bottom to top.
			for display_str in display_str_list:
				text_width, text_height = font.getsize(display_str)
				margin = np.ceil(0.05 * text_height)
				draw.rectangle(
					[(left, text_bottom + text_height + 2 * margin), (left + text_width,
						text_bottom)],
					fill='red')
				draw.text(
					(left + margin, text_bottom),
					display_str,
					fill='black',
					font=font)
				text_bottom += text_height + margin

	# Copies the new image into the one that was passed in
	np.copyto(image, np.array(image_pil))
