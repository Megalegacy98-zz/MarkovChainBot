import random
import copy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file to get data from", type=str)
parser.add_argument("paragraphs", help="Number of paragraphs to generate", type=int)
parser.add_argument("--size", help="Size of the paragraphs", type=int)

args = parser.parse_args()

final_sentence = ""
input = open(args.input, "r")


def fix_up_input(input):
	words = input.read().strip().replace('\n', ' ').replace('.','').replace('"','').lower().split(' ')

	list_of_words = []

	for word in words:
		if word == '' or word == '\n':
			continue
		list_of_words.append(word.strip())
	
	input.seek(0)
	
	return list_of_words

def get_random_phrase(input):
	phrases = {}
	word_base = 2
	
	phrases_list = []
	two_compare = []
	
	list_of_words = fix_up_input(input)
	max_index = len(list_of_words) - word_base
	random_index = random.randrange(0, max_index)
	
	selected_word = list_of_words[random_index]
	
	for word in range(0, max_index):
		# if the word is the selected word we chose
		if list_of_words[word] == selected_word:
			phrase = ""
			# compile a phrase
			for index in range(0, word_base+1):
				phrase += list_of_words[word+index]
				phrase += " "
			
			# get rid of extra whitespace
			phrase = phrase[:len(phrase)-1]
			
			# if it's already in the phrases dictionary
			if phrase in phrases:
				# add weight to it
				phrases[phrase] += 1
			else:
				# set a weight
				phrases[phrase] = 1
				phrases_list.append(phrase)
	
	# if the amount of phrases is equal to one
	if len(phrases_list) == 1 or len(phrases) == 1:
		# we don't need to use probability
		return phrases_list[0]
			
	# get the comparing/probability part ready
	two_compare.append(phrases_list[0])		
	two_compare.append(phrases_list[1])
			
	first_word = two_compare[0]
	second_word = two_compare[1]
	for word in range(0, len(phrases_list)+1):
		
		#print(str(phrases[first_word]) + " vs " + str(phrases[second_word]))
		
		whole = phrases[first_word] + phrases[second_word]
		probability = phrases[first_word] / whole
		
		num = random.random()
		
		# if the random percentage is in the zone of the foreign digit
		if probability <= num:
			
			# replace the winner digit with the foreign digit
			first_word = second_word
			
			# get a foreign digit in there (if possible)
			if word != len(phrases_list):
				second_word = phrases_list[word] 
			
		# if the random percentage is in the zone of the winner digit
		elif probability > num:
			
			# just grab another foreign digit
			if word != len(phrases_list):
				second_word = phrases_list[word]
	
	return(first_word)

size = args.size

# if size wasn't specified
if(size == None):
	# specify a size
	size = 20
else:
	# keep the current size
	size = args.size
	
final_string = ""

for paragraph in range(0, args.paragraphs):
	para = ""
	# for each index in a random number between 10 and size
	for a in range(random.randint(10, size)):
		# if index is 0
		if(a == 0):
			# make first sentence have upper case letter
			para += get_random_phrase(input)
			para = para[0].upper() + para[1:]
			para += " "
		else:
			# do it normally
			para += get_random_phrase(input)
			para += " "
	# replace whitespace with period
	para = para[:len(para)-1] + "."
	# spacing in between
	para += "\n\n"
	
	# add it to the final product
	final_string += para


	
print(final_string)

input.close()
