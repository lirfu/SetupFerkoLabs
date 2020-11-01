#!/usr/bin/env python3

###
# Copy and unzip students' Ferko uploads into designated term folders. 
#
# Joint Ferko zip must be unpacked as a folder 'uploads'.
# Each term mus be a folder of name satisfying regex '[0-9]{1,2}-[0-9]{1,2}.*' and contain CSV/TSV/SSV list of students in file named 'popis.txt', JMBAGs as first column.
# Script copies all files from the unpacked Ferko bank based on JMBAG of students in 'popis.txt' files.
#
# All logs are exported into 'result.log' for later inspection, including successes and errors: missing zips, missing folder, other exceptions.
#
# Example structure:
# 19-09-term1/
# -> popis.txt
# 19-10-term2/
# -> popis.txt
# uploads/
# -> 0036123456/
# ---> 0036123456.zip
# -> 0036234567/
# -> ...
###

import re
import shutil
import zipfile as zipp
import sys
import os
from os import path
import argparse


class Logger:
	def __init__(self, path):
		self.err = None
		self.path = path

	def log(self, s, quiet=False):
		if not quiet:
			print(s)
		if not self.err:
			self.err = open(self.path, 'w')
		self.err.write(s + '\n')

	def close(self):
		if self.err:
			self.err.close()


def copytermin(terminname, jmbags, remove=False):
	print(terminname, jmbags)
	try:
		if remove:
			log.log('---> Removing: {}'.format(terminname))
		else:
			log.log('---> Copying to: {}'.format(terminname))

		for idx in jmbags:
			src = path.join(database, idx)
			tar = path.join(terminname, idx)

			if remove:
				try:
					shutil.rmtree(tar)
					log.log('Success: \'{}\''.format(tar))
				except OSError as e:
					log.log('~> Caught \'OSError\' error: {}'.format(e))
				continue

			if not path.exists(src):
				log.log('! Source does not exist: {}'.format(src))
				continue
			if path.exists(tar):

				log.log('* Target already exists: {}'.format(tar))
				continue

			shutil.copytree(src, tar)

			try:
				zipf = None
				for fil in os.listdir(tar):
					if zipf:
						raise IOError('Found multiple files: {}, {}, [...]'.format(zipf, fil))
					zipf = fil
				zipf = path.join(tar, zipf)

				with zipp.ZipFile(zipf, 'r') as zip_ref:
					zip_ref.extractall(tar)
			except:
				log.log('! Error unzipping {}: {}'.format(tar, sys.exc_info()))
				continue

			log.log('Success: \'{}\''.format(tar))
	except IOError as e:
		log.log('~> Caught \'IOError\' error: {}'.format(e))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Copy and unzip students Ferko uploads into designated term folders. ')
	parser.add_argument('--version', action='version', version='%(prog)s 1.1')
	parser.add_argument('uploads', metavar='UPL_DIR', type=str, nargs='?', const='uploads', default='uploads', help='Folder containing unzipped bank of student uploads. Downloaded from Ferko site of current lab assignment. (Default: \'uploads\')')
	parser.add_argument('students', metavar='STUD_FILE', type=str, nargs='?', const='../students.csv', default='../students.csv', help='File containing information about students. Downloaded from course site as CSV list of grades. (Default: \'../students.csv\')')
	parser.add_argument('listfile', metavar='FILE', type=str, help='Filename of terms and jmbags in them.')
	parser.add_argument('--clear', action='store_true', help='Remove data copied to folders (revert the proccess of copying and extraction).')

	args = vars(parser.parse_args())

	log = Logger('result.log')
	table = Logger('table.csv')

	database = args['uploads']
	clear = args['clear']

	# Collect student information.
	studenti = {}
	with open(args['students']) as f:  # List of all students (svi studenti iz CSV popisa bodova predmeta).
		for l in f:
			parts = re.split(';', l.strip())
			studenti[parts[0]] = parts[0] + '\t' + parts[2][1:-1] + '\t' + parts[1][1:-1] + '\t' + parts[3][1:-1]

	with open(args['listfile'], 'r') as f:
		for l in f:
			parts = re.split('\|', l.strip())
			folname = parts[2][5:10] + '_' + parts[3][0:2] + '-' + parts[3][3:5]
			if not os.path.exists(folname):
				os.mkdir(folname)
			jmbags = re.split(' ', parts[7])
			copytermin(folname, jmbags, clear)
			for j in jmbags:
				if j not in studenti:
					table.log('!!! Unknown JMBAG:' + j, True)
				else:
					table.log(parts[2] + '\t' + parts[3] + '\t' + studenti[j], True)
			table.log('', True)

	log.close()
