import scrabble
import itertools
import time

directions = [-1, 0, 1]

class Letter:
	def __init__(self, letter, index):
		self.letter = letter
		self.x = index%4
		self.y = index/4
		self.index = index
		self.adjacent = []

	def find_adjacents(self, board):
		board.sort()
		for letter in board:
			if abs(letter.x-self.x) <=1 and abs(letter.y-self.y) <= 1 and letter != self:
				self.adjacent.append(letter)

	def __lt__(self, other):
		if self.index < other.index:
			return True
		else:
			return False

	def __str__(self):
		return self.letter

	def __eq__(self, other):
		if self.index == other.index:
			return True
		else:
			return False

	def __ne__(self, other):
		result = self.__eq__(other)
		return not result

class Board:

	def __init__(self, letterString, listWords):
		self.words = []
		self.dictionary = listWords
		self.letterString = letterString
		self.board = []
		for i in range(0,16):
			self.board.append(Letter(letterString[i], i))

	def printBoard(self):
		for letter in self.board:
			if letter.x == 3:
				print letter
			else:
				print letter,

	def populateAdjacents(self):
		for letter in self.board:
			letter.find_adjacents(self.board)

	def generateWordsRecurse(self, word, letter, usedLetters):
		# print "Word:", word+str(letter)
		# print "Adjacents:",
		# for temp in letter.adjacent:
		# 	print temp,
		# print
		# print "Used:",
		# for temp in usedLetters:
		# 	print temp,
		# print "\n==========\n"
		searchResult = scrabble.binary_search(word+str(letter), self.dictionary, False)
		#print searchResult
		usedLetters = usedLetters[:]
		usedLetters.append(letter)
		if searchResult[1] == True and len(word+str(letter)) >=3 and (word+str(letter)) not in self.words:
			self.words.append(word+str(letter))
		if searchResult[0] == True:
			for nextLetter in letter.adjacent:
				if nextLetter not in usedLetters:
					self.generateWordsRecurse(word+str(letter), nextLetter, usedLetters)
		else:
			return


	def generateWords(self):
		for letter in self.board:
			self.generateWordsRecurse("", letter, [])
		for i in range(0,len(self.words)):
			if i%4 == 0:
				print self.words[i]
			else:
				print self.words[i],


if __name__ == "__main__":
	dictionary = open("ospd.txt")

	listWords = []

	for line in dictionary: 
		line = line.split();
		listWords.append(line[0])

	userInput = raw_input("\nPlease input your letters: ")

	board = Board(userInput, listWords)
	board.printBoard()
	board.populateAdjacents()
	board.generateWords()

