import os
import argparse
import logging
import time
import numpy as np
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.INFO)

_description = 'The program "letter_count.py" has the main goal to return the frequency of each letter of the alphabet (without distinction between upper and lower case) in a text specified in the command line as an input file and also provides options to print a histogram and to print the basic stats of the text (e.g., number of characters, number of words, number of lines, etc.). This program also prints out the total elapsed time.'

def process(file_path,histo,stats):
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
	letters = 'abcdefghijklmnopqrstuvwxyz'
	frequency_dict = {}
	if stats:
		punctuation = '\|!"£$%&/()=?^,;.:-_[]#'
		punctuation_dict={} #creates a similar dictionary to the one used for the letters (only if the '-S' option is provided)
		for punct in punctuation:
			punctuation_dict[punct]=0
		numbers = '0123456789'
		numbers_dict={}
		for num in numbers:
			numbers_dict[num]=0
	for ch in letters:
		frequency_dict[ch]=0

	#Loop over the actual data.
	logging.info('Looping over the input text')
	if stats:
		isletter=0 #variable used to store the identity of the previous character in the loop (in order to count words, so that when a character isn't a letter AND the previous one is, it means that the program looped over a word, so that if I have two characters that aren't letter the program doesn't count it as a word)
		wordcounter=0
		linecounter=0
		isline=0 #same as 'isletter' but with '\n' (so that the program doesn't count as lines two or more '\n' in a row and counts only the lines with text)
		isnumber=0
		numbercounter=0
	for ch in data.lower():
		try:
			frequency_dict[ch]+=1
			if stats:
				isletter=1 #the current character is a letter
				isline=1 #the current line has text
				if isnumber==1:
					numbercounter+=1
				isnumber=0
		except KeyError:
			if stats:
					try:
						numbers_dict[ch]+=1
						isnumber=1
						isline=1
					except KeyError:
						if (ch==' ') or (ch=='\t') or (ch=='\''):
							if isletter==1:
								wordcounter+=1
							isletter=0
							if isnumber==1:
								numbercounter+=1
							isnumber=0
						if (ch=='\n'):
							if isletter==1:
								wordcounter+=1
							isletter=0
							if isnumber==1:
								numbercounter+=1
							isnumber=0
							if isline==1:
								linecounter+=1
							isline=0
						try:
							punctuation_dict[ch]+=1
						except:
							pass
			pass
	num_characters= float(sum(frequency_dict.values()))
	if histo:
		frequency=[] #creates an array with the occurences from the dictionary
		for ch in letters:
			frequency.append(frequency_dict[ch])
		indices = np.arange(len(letters)) #creates an array of len(letters) elements and each element is the i-th number of the array (indices[i]=i)
		plt.bar(indices, frequency, color='r') #y-axis
		plt.xticks(indices, letters) #assigns to each number in indices the corresponding character
		plt.ylabel('Occurences')
	#Normalize occurences
	for ch in letters:
		frequency_dict[ch]=frequency_dict[ch]/num_characters
	print(frequency_dict)
	if stats:
		logging.info('Printing some basic stats of the book:')
		print(punctuation_dict)
		print('Total occurences of punctuation=',sum(punctuation_dict.values()))
		print('Number of characters=',len(data))
		print('Number of letters=',int(num_characters))
		print('Number of words=',wordcounter)
		print('Number of lines=',linecounter)
		print(numbers_dict)
		print('Total number of numbers=',numbercounter)
	elapsed_time=time.time()-start_time	
	print('Elapsed time =',elapsed_time, 's')
	if histo:
		plt.show() #Shows the histogram (inserted here because the command finishes once the histogram is closed, so it prevents other commands from being executed)

if __name__=='__main__':
	parser = argparse.ArgumentParser(description=_description)
	parser.add_argument('infile',help='path to input text file')
	parser.add_argument('-H','--histo',dest='HISTO',action='store_true',help='show histogram of the occurences')
	parser.add_argument('-S','--stats',dest='STATS',action='store_true',help='show some basic stats of the book') #added two optional arguments ('action' is set to 'store_true' so that the option works only if the option is given, it doesn't need any additional parameter)
	args = parser.parse_args()
	process(args.infile,args.HISTO,args.STATS)
