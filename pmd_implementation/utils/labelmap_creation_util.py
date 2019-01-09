from object_detection.utils import label_map_util
import os

class LabelmapManager():
	
	def __init__(self, path: str):
		self.path = path
		self.labelmap_dict = label_map_util.get_label_map_dict(path) if os.path.exists(path) else { 'background':0 }

	def add_label(self, label: str):
		"""Adds a label to the dictionary,
		assigning it an id using the label map util
		returns the new id of the label
		returns None if the label already exists"""

		if not label in self.labelmap_dict:

			# Creates the new id
			label_id = label_map_util.get_max_label_map_index(self.labelmap_dict) + 1
			self.labelmap_dict[label] = label_id

			return label_id
		else:
			return None

	def convert_to_string(self):
		"""Converts the labelmap dictionary 
		into a string"""

		map_string = ""

		for k in self.labelmap_dict.keys():
			if k is not 'background':
				map_string += "item {\n\tid: " + self.labelmap_dict[k] + "\n\tname: '" + k + "'\n}\n"

		return map_string

	def write_to_file(self):
		"""Writes the current labelmap dictionary
		to file using the path already supplied"""

		with open(path, 'w') as fid:
			fid.write(self.convert_to_string())
