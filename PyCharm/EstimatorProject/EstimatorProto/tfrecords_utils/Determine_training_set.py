from random import shuffle
import os, fnmatch, pathlib, shutil

def read_train_val():
	"""Reads the names of all image files from the ./images/raw/ directory and then
	splits it up into multiple parts to be used by training and testing
	int the typical 90%/10% ratio."""
	
	# Maps the directory for image files and reads in all of the lines and then shuffles them
	files = list(map(lambda x: "./images/raw/" + x, fnmatch.filter(os.listdir("./images/raw/"), "*.jpg")))
	shuffle(files)
	
	for name in files:
		print(name)
	
	# Splits the files into two arrays of train values, and test values
	split_loc = int(len(files) * 0.9)
	train_values = files[:split_loc]
	test_values = files[split_loc:]
	return (train_values, test_values)
	
def copy_files(file_list, dst):
	"""Copies a list of files to another directory"""
	for file in file_list:
		print("Copying " + file + " to " + dst)
		shutil.copy(file, dst)
	
if __name__ == '__main__':
	"""Separates the image files in the ./images/raw/ directory into two categories
	then moves them into two directories, ./images/train/, and ./images/test/."""

	# Reads in the trainval.txt file and shuffles its contents
	# Then splits it into training and testing values
	(train, test) = read_train_val()
	
	# Creates the train folder if it doesn't exist yet.
	pathlib.Path("./images/train/").mkdir(parents=True, exist_ok=True)
	
	# Creates the test folder if it doesn't exist yet.
	pathlib.Path("./images/test/").mkdir(parents=True, exist_ok=True)
	
	# Copies the files into their respective directories
	copy_files(train, "./images/train/")
	copy_files(test, "./images/test/")