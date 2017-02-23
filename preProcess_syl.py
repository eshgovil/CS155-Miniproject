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

# lists of the words for all splits
quatrainWords = []
coupletWords = []
voltaWords = []
stanzaWords = []

# lists of syllables for all splits
quatrainSyl = []
coupletSyl = []
voltaSyl = []
stanzaSyl = []

# list of lists of words
quatrains = []
couplets = []
voltas = []
stanzas = []

# hash table mapping each word to words that rhyme to it
rhymes = {}

f_shake = open('./project2data/shakespeare.txt')

shakeLines = f_shake.readlines()

curLineinPoem = 0
curQuatrain = []
curCouplet = []
curVolta = []
curStanza = []
curQuatrainSyl = []
curCoupletSyl = []
curVoltaSyl = []
curStanzaSyl = []

rhymeA = "";
rhymeB = "";

for i, line in enumerate(shakeLines):
	if line == '\n':
		continue

	words = word_tokenize(line)

	# get rid of all punctuations
	for elem in words:
		if elem in string.punctuation:
			words.remove(elem)

	# because the sonnets are numbered in the doc, when a 
	# number appears, everything stored before that can be added
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
		curQuatrainSyl = []
		curCoupletSyl = []
		curVoltaSyl = []
		curStanzaSyl = []
		continue

	# Build dictionary of rhymes
	if curLineinPoem < 12:
		# get the first rhyming word in the stanza
		if (curLineinPoem % 4 == 0):
			rhymeA = words[-1]
		# for the second rhyme in the stanza
		if (curLineinPoem % 4 == 2):
			# check the first rhyme is there
			if rhymeA in rhymes.keys():
				# check if the current second rhyme is not already a key
				if (words[-1] not in rhymes[rhymeA]):
					# add that rhyme to the key for the first rhyme
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
	# build rhyme for couplet
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

	# build lists of words for stanzas, quatrains, etc
	if curLineinPoem < 4 or (curLineinPoem > 8 and curLineinPoem < 12):
		quatrainWords += words
		curQuatrain += words
		stanzaWords += words
		curStanza += words
		if curLineinPoem % 4 != 3:
			curQuatrain += ['\n']
			curStanza += ['\n']
	elif curLineinPoem > 4 and curLineinPoem <= 8:
		voltaWords += words
		curVolta += words
		stanzaWords += words
		curStanza += words
		if curLineinPoem != 8:
			curVolta += ['\n']
			curStanza += ['\n']
	else:
		coupletWords += words
		curCouplet += words
		if curLineinPoem != 13:
			curCouplet += ['\n']
	curLineinPoem += 1

	# get rid of all punctuations
	for elem in words:
		if '\'' in elem or '-' in elem:
			words.remove(elem)

	# build lists of syllables for stanzas, quatrains, etc
	syllables = []
	if curLineinPoem < 4 or (curLineinPoem > 8 and curLineinPoem < 12):
		for word in words:
			try:
				syllables += d[word.lower()][0]
				print(nsyl(word))
			except KeyError:
				syllables += ['NULL']
		quatrainSyl += syllables
		curQuatrainSyl += syllables
		stanzaSyl += syllables
		curStanzaSyl += syllables
		if curLineinPoem % 4 != 3:
			curQuatrainSyl += ['\n']
			curStanzaSyl += ['\n']
	elif curLineinPoem > 4 and curLineinPoem <= 8:
		voltaSyl += syllables
		curVoltaSyl += syllables
		stanzaSyl += syllables
		curStanzaSyl += syllables
		if curLineinPoem != 8:
			curVoltaSyl += ['\n']
			curStanzaSyl += ['\n']
	else:
		coupletSyl += syllables
		curCoupletSyl += syllables
		if curLineinPoem != 13:
			curCoupletSyl += ['\n']
	curLineinPoem += 1

print (quatrainSyl)

# Use MultinomialHMM
