# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import argparse
import tempfile
import logging
from xml.etree import ElementTree
from xml.dom import minidom

from image_processing import conversion, validation, kakadu, openjpeg
from jpylyzer.jpylyzer import checkOneFile
from PIL import Image, ImageCms

VALID_EXTENSIONS = [".jpg", ".jpeg", ".tif", ".tiff", ".JPG", ".JPEG", ".TIF", ".TIFF", '.png', '.PNG']
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


class Jp2Converter(object):

	def __init__(self, input_dir, output_dir, encoder, bin_path, validate_jp2):
		self.input_dir = os.path.abspath(input_dir)
		self.output_dir = os.path.abspath(output_dir)
		self.encoder = encoder
		self.bin_path = bin_path
		self.validate_jp2 = validate_jp2

	def convert(self):
		if not os.path.isdir(self.output_dir):
			os.mkdir(self.output_dir)

		files_to_process = [os.path.join(self.input_dir, f) for f in os.listdir(self.input_dir) if self.__filter_fnames(f)]
		invalids = []
		total = len(files_to_process)
		for image in files_to_process:
			filename = os.path.basename(image)
			filename, ext = os.path.splitext(filename)
			input_file = os.path.join(self.input_dir, "{0}{1}".format(filename, ext))
			output_file = os.path.join(self.output_dir, "{0}.jp2".format(filename))
			temp_tiff_filepath = None

			if ext == '.jpg':
				# convert jpg to a temp tiff (required by Kakadu)
				converter = conversion.Converter()
				with tempfile.NamedTemporaryFile(prefix='image-processing_', suffix='.tif', delete=False) as temp_tiff_file_obj:
					temp_tiff_filepath = temp_tiff_file_obj.name
					converter.convert_to_tiff(input_file, temp_tiff_filepath)
					input_file = temp_tiff_filepath

			# openjpeg encoder selected
			if self.encoder == 'opj':
				opj = openjpeg.OpenJpeg(openjpeg_base_path=self.bin_path)
				opj.opj_compress(input_file, output_file, openjpeg_options=openjpeg.DEFAULT_LOSSLESS_COMPRESS_OPTIONS)
			# kakadu encoder selected
			elif self.encoder == 'kdu':
				kdu = kakadu.Kakadu(kakadu_base_path=self.bin_path)
				kdu.kdu_compress(input_file, output_file, kakadu_options=kakadu.DEFAULT_LOSSLESS_COMPRESS_OPTIONS)
				#opts = kakadu.DEFAULT_COMPRESS_OPTIONS + kakadu.LOSSY_OPTIONS
				#kdu.kdu_compress(input_file, output_file, kakadu_options=opts)

			if self.validate_jp2:
				if not self.__is_valid_jp2(output_file):
					invalids.append(output_file)

			# Remove the temp tiff file
			if temp_tiff_filepath is not None:
				os.unlink(temp_tiff_filepath)
				assert not os.path.exists(temp_tiff_filepath)

		self.__report_msg(total, invalids)

	def __report_msg(self, total, invalids):
		print('-----------------------')
		print('# {0} images have been converted successfully to JP2'.format(total))
		if len(invalids):
			print('# These images are not valid JP2:')
			print('\n'.join(invalids))

	def __is_valid_jp2(self, image_path, output_file=None):
		""" derived from image_processing.conversion.validate_jp2 """
		logger = logging.getLogger(__name__)
		jp2_element = checkOneFile(image_path)
		success = jp2_element.findtext('isValidJP2') == 'True' or jp2_element.findtext('isValid') == 'True'
		output_string = minidom.parseString(ElementTree.tostring(jp2_element)).toprettyxml(encoding='utf-8')
		if output_file:
			with open(output_file, 'wb') as f:
				f.write(output_string)
		return False if not success else True

	def __filter_fnames(self, fname):
		if fname.startswith('.'):
			return False
		if fname.startswith('_'):
			return False
		if fname == "Thumbs.db":
			return False
		if os.path.splitext(fname)[-1].lower() not in VALID_EXTENSIONS:
			return False
		return True


def main(argv):
	parser = argparse.ArgumentParser(description='Convert images in a folder to JP2')
	parser.add_argument('-i', '--input_dir', help='Choose input directory', required=True, default=None)
	parser.add_argument('-o', '--output_dir', help='Choose output directory', required=True, default=None)
	parser.add_argument('--with-openjpeg', help='Select OpenJPEG encoder', action='store_true')
	parser.add_argument('--with-kakadu', help='Select Kakadu encoder (default)', action='store_true')
	parser.add_argument('-b', '--binary-path', help='Base path to openjpeg or kakadu executables (default: /usr/local/bin', required=False, default='/usr/local/bin')
	parser.add_argument('--validate-jp2', help='Validate generated JP2 files?', action='store_true')
	args = parser.parse_args()
	input_dir = args.input_dir
	output_dir = args.output_dir
	if args.with_openjpeg:
		encoder = 'opj'
	elif args.with_kakadu:
		encoder = 'kdu'
	else:
		encoder = 'kdu'
	bin_path = args.binary_path
	validate_jp2 = args.validate_jp2
	# print summary
	print('# Input directory:\t {0}'.format(input_dir))
	print('# Output directory:\t {0}'.format(output_dir))
	if encoder == 'opj':
		print('# OpenJPEG encoder will be used, from {0}'.format(bin_path))
	elif encoder == 'kdu':
		print('# Kakadu encoder will be used (default), from {0}'.format(bin_path))
	if validate_jp2:
		print('# All JP2 files will be validated with Jpylyzer')
	# call convert task
	c = Jp2Converter(input_dir, output_dir, encoder, bin_path, validate_jp2)
	c.convert()

if __name__ == "__main__":
	main(sys.argv[1:])
	sys.exit(0)