import sys, time, pandas as pd
import nltk
from nltk.corpus import cmudict
import nltk.data
import string
from nltk.tokenize import sent_tokenize, word_tokenize

# Start the timer
start = time.time()

#nltk.download()
d = cmudict.dict()

# taken from somewhere
def nsyl(word):
      return max([len([y for y in x if y[-1].isdigit()]) for x in d[word.lower()]])

quatrainWords = []
coupletWords = []
voltaWords = []
stanzaWords = []

quatrains = []
couplets = []
voltas = []
stanzas = []

rhymes = {}

f_shake = open('./project2data/shakespeare.txt')

shakeLines = f_shake.readlines()

curLineinPoem = 0
curQuatrain = []
curCouplet = []
curVolta = []
curStanza = []

rhymeA = "";
rhymeB = "";

for i, line in enumerate(shakeLines):
	if line == '\n':
		continue

	words = word_tokenize(line)

	for elem in words:
		if elem in string.punctuation:
			words.remove(elem)

	if words[0].isdigit():
		quatrains.append(curQuatrain)
		voltas.append(curVolta)
		couplets.append(curCouplet)
		stanzas.append(curStanza)
		curLineinPoem = 0
		curQuatrain = []
		curCouplet = []
		curVolta = []
		curStanza = []
		continue

	# Build dictionary of rhymes
	if curLineinPoem < 12:
		if (curLineinPoem % 4 == 0):
			rhymeA = words[-1]
		if (curLineinPoem % 4 == 2):
			if rhymeA in rhymes.keys():
				if (words[-1] not in rhymes[rhymeA]):
					rhymes[rhymeA].append(words[-1])
			else:
				rhymes[rhymeA] = [words[-1]]
			if words[-1] in rhymes.keys():
				if (rhymeA not in rhymes[words[-1]]):
					rhymes[words[-1]].append(rhymeA) 
			else:
				rhymes[words[-1]] = [rhymeA]

		if (curLineinPoem % 4 == 1):
			rhymeB = words[-1]
		if (curLineinPoem % 4 == 3):
			if rhymeB in rhymes.keys():
				if (words[-1] not in rhymes[rhymeB]):
					rhymes[rhymeB].append(words[-1])
			else:
				rhymes[rhymeB] = [words[-1]]
			if words[-1] in rhymes.keys():
				if (rhymeB not in rhymes[words[-1]]):
					rhymes[words[-1]].append(rhymeB) 
			else:
				rhymes[words[-1]] = [rhymeB]
	else:
		if (curLineinPoem == 12):
			rhymeG = words[-1]
		if (curLineinPoem == 13):
			if rhymeG in rhymes.keys():
				if (words[-1] not in rhymes[rhymeG]):
					rhymes[rhymeG].append(words[-1])
			else:
				rhymes[rhymeG] = [words[-1]]
			if words[-1] in rhymes.keys():
				if (rhymeG not in rhymes[words[-1]]):
					rhymes[words[-1]].append(rhymeG) 
			else:
				rhymes[words[-1]] = [rhymeG]

	if curLineinPoem < 4 or (curLineinPoem > 8 and curLineinPoem < 12):
		quatrainWords += words
		curQuatrain += words
		if curLineinPoem % 4 != 3:
			curQuatrain += ['\n']
	elif curLineinPoem > 4 and curLineinPoem <= 8:
		voltaWords += words
		curVolta += words
		if curLineinPoem != 8:
			curVolta += ['\n']
	else:
		coupletWords += words
		curCouplet += words
		if curLineinPoem != 13:
			curCouplet += ['\n']
	stanzaWords += words
	curStanza += words
	if curLineinPoem != 13:
		curStanza += ['\n']
	curLineinPoem += 1

#print (quatrains)

# Use MultinomialHMM
