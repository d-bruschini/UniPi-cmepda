import os
import argparse
import logging
import time
logging.basicConfig(level=logging.INFO)

_description = 'The program "letter_count.py" has the main goal to return the frequency of each letter of the alphabet (without distinction between upper and lower case) in a text specified in the command line as an input file and also provides options to print a histogram, skip specific parts of the text and print the basic stats of the text (e.g., number of characters, number of words, number of lines, etc.). This program also prints out the total elapsed time.'

def process(file_path):
	"""Main processing routine
	"""
	#basic sanity checks
	assert file_path.endswith('.txt') #checks if the file_path ends with .txt
	assert os.path.isfile(file_path) #checks if the file is in the filesystem
	
	#if good open file	
	start_time=time.time()
	logging.info('Opening file %s...', file_path)
	with open(file_path) as input_file:
		data=input_file.read() #file is automatically closed at the exit. ALWAYS open files with 'with'
	logging.info('Done. %d characters found.', len(data))
	
	#Initialize dictionary with lower case letters
	letters = 'abcdefghijklmnoprstuvwxyz'
	frequency_dict = {}
	for ch in letters:
		frequency_dict[ch]=0

	#Loop over the actual data.
	logging.info('Looping over the input text')
	for ch in data.lower():
		try:
			frequency_dict[ch]+=1
		except KeyError:
			pass
	num_characters= float(sum(frequency_dict.values()))
	#Normalize occurences
	for ch in letters:
		frequency_dict[ch]=frequency_dict[ch]/num_characters
	print(frequency_dict)
	elapsed_time=time.time()-start_time
	print('Elapsed time =',elapsed_time, 's')

if __name__=='__main__':
	parser = argparse.ArgumentParser(description=_description)
	parser.add_argument('infile',help='path to input text file')
	args = parser.parse_args()
	process(args.infile)
