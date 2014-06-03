import itertools
import time



#### OUT DATED FUNCTIONS ############################################

# def find_subsets(mylist, subsets):
# 	oldsubsets = []
# 	for item in subsets:
# 		oldsubsets.append(list(item))
# 		item.append(mylist[-1]);
# 	subsets = oldsubsets + subsets
# 	mylist.pop()
# 	if mylist == []:
# 		return subsets
# 	else:
# 		return find_subsets(mylist, subsets)


# def useboard(letters, listwords):
# 	boardword = raw_input("Please input a word from the board. ")
# 	cumulated_answers = []
# 	for letter in boardword:
# 		templetters = list(letters)
# 		templetters.append(letter)
# 		#print "Using " + letter
# 		cumulated_answers+=find_allwords(templetters, listwords)
# 		#print boardword
# 		if boardword == "":
# 			return
# 		else:
# 			boardword = boardword[1:]
# 	set(cumulated_answers)
# 	list(cumulated_answers)
# 	cumulated_answers.sort(lambda x,y: cmp(len(x), len(y)))
# 	for word in cumulated_answers:
# 		print len(word), word

# def find_allwords(letters, listWords):
# 	subsets = [[]]
# 	subsets = find_subsets(letters, subsets)

# 	permutations = []

# 	possibilities = []

# 	for i in range(len(subsets)):
# 		#print i, len(subsets)
# 		#print subsets[i]
# 		permutations = (list(itertools.permutations(subsets[i])))
# 		permutations = set(permutations)
# 		permutations = list(permutations)
# 		for word in permutations:
# 			word = "".join(list(word))
# 			possibilities.append(word)

# 	#possibilities.sort(lambda x,y: cmp(len(x), len(y)))

# 	answers = []
# 	for word in possibilities:
# 		if word in listwords:
# 			answers.append(word)

# 	return answers

########################################################################


answers_global = []
letter_value_global = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3, "n": 1, "o":1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10 }
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z"]
words_and_scores = {}

# BINARY_SEARCH
#
# Searches a sorted dictionary for a word. If the word is a partial match, the function returns a tuple with (True, False)
# if it is a perfect match, returns (True, True)

def binary_search(word, listWords, partialFound):
	if len(listWords) == 0:
		return (False, False)
	if len(listWords) == 1:
		if word == listWords[0][:len(word)]:
			partialFound = True
			if word == listWords[0]:
				return (partialFound, True)
			else:
				return (partialFound, False)
		else:
			return (partialFound, False)
	else:
		if word == listWords[len(listWords)/2][:len(word)]:
			if word == listWords[len(listWords)/2]:
				return (True, True)
			else:
				partialFound = True
				return binary_search(word, listWords[:len(listWords)/2], partialFound)
		elif word < listWords[len(listWords)/2]:
			return binary_search(word, listWords[:len(listWords)/2], partialFound)
		elif word > listWords[len(listWords)/2]:
			return binary_search(word, listWords[len(listWords)/2:], partialFound)
		
# GENERATE_WORDS_RECURSE
#
# Helper function to "generate_words", recursively builds words and checks them against a word bank using "binary_search"

def generate_words_recurse(letters, partialWord, letterToAdd, listWords):
	if letterToAdd == ".":
		gwrLetters = list(letters)
		gwrLetters.remove(letterToAdd)
		for newLetter in alphabet:
			wordSearch = binary_search(partialWord+newLetter, listWords, False)
			if wordSearch[0]:
				if wordSearch[1]:
					answers_global.append(partialWord+newLetter)
				if gwrLetters == []:
						continue
				else:
					for letter in gwrLetters:
						generate_words_recurse(gwrLetters, partialWord+newLetter, letter, listWords)
		return
	else:
		gwrPartialWord = partialWord + letterToAdd
		gwrLetters = list(letters)
		gwrLetters.remove(letterToAdd)
		wordSearch = binary_search(gwrPartialWord, listWords, False)
		if wordSearch[0]:
			if wordSearch[1]:
				answers_global.append(gwrPartialWord)
			if gwrLetters == []:
					return
			else:
				for letter in gwrLetters:
					generate_words_recurse(gwrLetters, gwrPartialWord, letter, listWords)
				return
		else:
			return


# GENERATE_MATCH_RECURSE
#
# Generates matches for generate_match

def generate_match_recurse(letters, partialWord, letterToAdd, boardWord, listWords):
	#print partialWord, boardWord
	
	if boardWord != "" and boardWord[0] != "_":
		#print "|"+ partialWord +"|" + letterToAdd + "|" + boardWord + "|"
		gmrLetters = list(letters)
		gmrPartialWord = partialWord + boardWord[0]
		#print gmrPartialWord
		gmrBoardWord = boardWord[1:]
		wordSearch = binary_search(gmrPartialWord, listWords, False)
		gmrLetterToAdd = str(letterToAdd)
		if wordSearch[0]:
			#print "its a match"
			if wordSearch[1]:
				answers_global.append(gmrPartialWord)
			generate_match_recurse(gmrLetters, gmrPartialWord, gmrLetterToAdd, gmrBoardWord, listWords)
			return
		else:
			return
	elif letterToAdd == "":
		return
	
	elif (boardWord != "" and boardWord[0] == "_") or letters != []:
		#print "|"+ partialWord +"|" + letterToAdd + "|" + boardWord + "|"
		if letterToAdd == ".":
			gmrLetters = list(letters)
			gmrLetters.remove(letterToAdd)
			gmrBoardWord = boardWord[1:]
			for newLetter in alphabet:
				wordSearch = binary_search(partialWord+newLetter, listWords, False)
				if wordSearch[0]:
					if wordSearch[1]:
						answers_global.append(partialWord+newLetter)
					if gmrLetters == [] and gmrBoardWord != "":
						generate_match_recurse(gmrLetters, partialWord+newLetter, "", gmrBoardWord, listWords)
						#return
					else:
						for letter in gmrLetters:
							generate_match_recurse(gmrLetters, partialWord+newLetter, letter, gmrBoardWord, listWords)
				#else:
				#	return
			return
		else:
			gmrPartialWord = partialWord + letterToAdd
			gmrBoardWord = boardWord[1:]
			gmrLetters = list(letters)
			gmrLetters.remove(letterToAdd)
			wordSearch = binary_search(gmrPartialWord, listWords, False)
			if wordSearch[0]:
				if wordSearch[1]:
					answers_global.append(gmrPartialWord)

				if gmrLetters == [] and gmrBoardWord != "":
					generate_match_recurse(gmrLetters, gmrPartialWord, "", gmrBoardWord, listWords)
					#return
				else:
					for letter in gmrLetters:
						generate_match_recurse(gmrLetters, gmrPartialWord, letter, gmrBoardWord, listWords)
					return
			else:
				return



# GENERATE_WORDS
#
# Generates words sequentially by adding a letter onto the previous word (uses helper function "generate_words_recurse")

def generate_words(letters, listWords):
	word = ""
	for letter in letters:
		#print letter
		generate_words_recurse(letters, word, letter, listWords)
	return

# GENERATE_MATCH
#
# Generates words to fit a template, e.g. with the letters "apy" and the template: "h__p", it will generate "happy"

def generate_match(letters, boardWord, listWords):
	boardWord = "_"*(len(letters)+1) + boardWord
	word = ""
	while boardWord[0] == "_":
		boardWord = boardWord[1:]
		for letter in letters:
			generate_match_recurse(letters, word, letter, boardWord, listWords)

# GENERATE_MATCH2_RECURSE
#
# Recursive helper for match2, in case of the suffix. 

def generate_match2_recurse(letters, partialWord, letterToAdd, suffix, listWords):
	if letterToAdd == ".":
		gwrLetters = list(letters)
		gwrLetters.remove(letterToAdd)
		for newLetter in alphabet:
			wordSearch = binary_search(partialWord+newLetter, listWords, False)
			if wordSearch[0]:
				if binary_search(partialWord+newLetter+suffix, listWords, False) == (True, True):
					answers_global.append(partialWord+newLetter+suffix)
				if gwrLetters == []:
						continue
				else:
					for letter in gwrLetters:
						generate_words_recurse(gwrLetters, partialWord+newLetter, letter, listWords)
		return
	else:
		gwrPartialWord = partialWord + letterToAdd
		gwrLetters = list(letters)
		gwrLetters.remove(letterToAdd)
		wordSearch = binary_search(gwrPartialWord, listWords, False)
		if wordSearch[0]:
			if binary_search(partialWord+newLetter+suffix, listWords, False) == (True, True):
					answers_global.append(partialWord+newLetter+suffix)
			if gwrLetters == []:
					return
			else:
				for letter in gwrLetters:
					generate_words_recurse(gwrLetters, gwrPartialWord, letter, listWords)
				return
		else:
			return

# GENERATE_MATCH2
#
# Generates words to fit a template, either a prefix or suffix or middlefix, e.g. with the letters "hy" and the middlefix "app", it will generate "happy"

def generate_match2(letters, boardWord, listWords):
	if boardWord[0] == "-" and boardWord[-1] == "-":
		tempLetters = list(letters)
		tempLetters.append(boardWord[1:-1])
		generate_words(tempLetters, listWords)
	elif boardWord[-1] == "-":
		for letter in letters:
			generate_words_recurse(letters, boardWord[:-1], letter, listWords)
	elif boardWord[0] == "-":
		word = ""
		for letter in letters:
			generate_match2_recurse(letters, word, letter, boardWord[1:], listWords)
	return


def generate_words_board(letters, boardWord, listWords):
	tempLetters = list(letters)
	
	if boardWord == "":
		generate_words(tempLetters, listWords)
	elif "-" in boardWord:
		generate_match2(letters, boardWord, listWords)
	elif "_" in boardWord:
		generate_match(letters, boardWord, listWords)
	else:
		for letter in boardWord:
			tempLetters.append(letter)
			generate_words(tempLetters, listWords)
			tempLetters.remove(letter)
	return




def adjacent_check_word(word, boardWord):
	originalWord = str(word)
	for letter in word:
		validPlay = False
		for i in range(len(boardWord)):
			if i < len(word):
				if binary_search(boardWord[i]+word[i], listWords, False) == (True, True):
					validPlay = True
				else:
					validPlay = False
					break
		if validPlay == True:
			print "You can play " + word + " behind " + boardWord + "."
		word = word[1:]

	word = str(originalWord)
	for letter in word:
		validPlay = False
		for i in range(len(boardWord)):
			if i < len(word):
				if binary_search(word[i]+boardWord[i], listWords, False) == (True, True):
					validPlay = True
				else:
					validPlay = False
					break
		if validPlay == True:
			print "You can play " + word + " in front of " + boardWord + "."
		word = word[1:]

def perpendicular_check_word(word, boardWord):
	for letter in word:
		if binary_search(letter+boardWord, listWords, False) == (True, True):
			validPlay = True
		else:
			validPlay = False
		if validPlay == True:
			print "You can play " + word + " on top of " + boardWord + "."

		if binary_search(boardWord+letter, listWords, False) == (True, True):
			validPlay = True
		else:
			validPlay = False
		if validPlay == True:
			print "You can play " + word + " underneath " + boardWord + "."

		word = word[1:]





def calculate_score():
	for word in answers_global:
		wordScore = 0
		for letter in word:
			wordScore += letter_value_global[letter]
		words_and_scores[word] = wordScore


def print_formatted():
	length = 0
	i = 0
	for word in answers_global:
		if len(word) != length:
			print "\n\n"+str(len(word)) + ":"
			length = len(word)
			i = 0
		if i == 5:
			print 
			i = 0
		i+=1
		print word + "\t",
	print

def print_formatted_calculated():
	length = 0
	i = 0
	calculate_score()
	for word in answers_global:
		if len(word) != length:
			print "\n\n"+str(len(word)) + ":"
			length = len(word)
			i = 0
		if i == 5:
			print 
			i = 0
		i+=1
		print  word + "-" + str(words_and_scores[word]) + "\t",
	print
	if answers_global == []:
		print "No answers found!"
		return
	find_max_score()

def find_max_score():
	maxScore = 0
	highWord = ""
	for word in words_and_scores:
		if words_and_scores[word] > maxScore:
			maxScore = words_and_scores[word]
			highWord = word
	print "\nHighScore: " + highWord + "-" + str(maxScore)

			



	


	

######## MAIN ###########
if __name__ == "__main__":
	dictionary = open("ospd.txt")

	listWords = []

	for line in dictionary: 
		line = line.split();
		listWords.append(line[0])


	while 1:
		while 1:
			start = time.clock()
			
			userInput = raw_input("\nPlease input your letters: ")
			if userInput == "":
				break
			userInput = userInput.split(" ")
			
			if len(userInput) > 1:
				boardWord = userInput[1]
			else: 
				boardWord = ""
			userInput = list(userInput[0])
			
			generate_words_board(userInput, boardWord, listWords)
			
			
			
			answers_global = set(answers_global)
			answers_global = list(answers_global)
			answers_global.sort(lambda x,y: cmp(len(x), len(y)))

			print_formatted_calculated()
			

			print "\nThis took: " + str(time.clock() - start) + " seconds. With a total number of words: " + str(len(answers_global))
			del answers_global[:]
			words_and_scores.clear()
		while 1:
			checkSwitch = raw_input("\nTo check a word, input the word and the word on the board, separated by a space: ")
			if checkSwitch != "":
				checkSwitch = checkSwitch.split(" ")
				if len(list(checkSwitch)) == 1:
					if binary_search(checkSwitch[0], listWords, False)[1]:
						print "\n" + checkSwitch[0] + " is a word."
				else:
					print "\nAs touching words: "
					adjacent_check_word(checkSwitch[0], checkSwitch[1])
					adjacent_check_word(checkSwitch[1], checkSwitch[0])
					print "\nAs perpendicular words, not crossing: "
					perpendicular_check_word(checkSwitch[0], checkSwitch[1])
					perpendicular_check_word(checkSwitch[1], checkSwitch[0])
			else:
				break

