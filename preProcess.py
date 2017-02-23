import sys, time, pandas as pd
import nltk
from nltk.corpus import cmudict
import nltk.data
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder
import json


<<<<<<< HEAD
nltk.download()
=======
# nltk.download()
>>>>>>> origin/master
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
f_spence = open('./project2data/spenser.txt')


out_quatrains= 'out_quatrains.csv' 
out_voltas = 'out_voltas.csv' 
out_couplets = 'out_couplets.csv'
out_rhymes = 'out_rhymes.json'
out_quatrain_w_to_i = 'out_q_w_map.json' 
out_volta_w_to_i = 'out_v_w_map.json' 
out_couplets_w_to_i = 'out_c_w_map.json'  

shakeLines = f_shake.readlines()
spenceLines = f_spence.readlines()

curLineinPoem = 0
curQuatrain = []
curCouplet = []
curVolta = []
curStanza = []

rhymeA = "";
rhymeB = "";
rhymeG = "";

# Build lists of quatrains, voltas, and couplets for Shakespeare's Poems
for i, line in enumerate(shakeLines):
<<<<<<< HEAD
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

print (quatrains)

# Use MultinomialHMM
=======
    if line == '\n':
        continue

    words = [x.lower() for x in word_tokenize(line)]

    prevElem = words[0]
    for i, elem in enumerate(words):
        if elem == "is" and prevElem == "'t": # Handle 'tis... unique case
            words[i - 1] = "'tis"
            words.remove(elem)
            elem = words[i - 1]
        elif elem == "'s": # Manually handle apostrophes
            words[i - 1] += "'s"
            words.remove(elem)
            elem = words[i - 1]
        elif elem == "'d": # Manually handle apostrophes
            words[i - 1] += "'d"
            words.remove(elem)
            elem = words[i - 1]
        elif elem in string.punctuation:
            words.remove(elem)
        prevElem = elem

    if words[0].isdigit():
        if (curQuatrain != []):
            quatrains.append(curQuatrain)
            voltas.append(curVolta)
            couplets.append(curCouplet)
            #stanzas.append(curStanza)
        curLineinPoem = 0
        curQuatrain = []
        curCouplet = []
        curVolta = []
        #curStanza = []
        continue

    # Build dictionary of rhymes
    if curLineinPoem < 12:
        lastWord = words[-1]
        if (curLineinPoem % 4 == 0):
            rhymeA = lastWord 
        if (curLineinPoem % 4 == 2):
            if rhymeA in rhymes.keys():
                if (lastWord  not in rhymes[rhymeA]):
                    rhymes[rhymeA].append(lastWord)
            else:
                rhymes[rhymeA] = [lastWord]
            if lastWord in rhymes.keys():
                if (rhymeA not in rhymes[lastWord]):
                    rhymes[lastWord].append(rhymeA) 
            else:
                rhymes[lastWord] = [rhymeA]

        if (curLineinPoem % 4 == 1):
            rhymeB = lastWord
        if (curLineinPoem % 4 == 3):
            if rhymeB in rhymes.keys():
                if (lastWord not in rhymes[rhymeB]):
                    rhymes[rhymeB].append(lastWord)
            else:
                rhymes[rhymeB] = [lastWord]
            if lastWord in rhymes.keys():
                if (rhymeB not in rhymes[lastWord]):
                    rhymes[lastWord].append(rhymeB) 
            else:
                rhymes[lastWord] = [rhymeB]
    else:
        if (curLineinPoem == 12):
            rhymeG = lastWord
        if (curLineinPoem == 13):
            if rhymeG in rhymes.keys():
                if (lastWord not in rhymes[rhymeG]):
                    rhymes[rhymeG].append(lastWord)
            else:
                rhymes[rhymeG] = [lastWord]
            if lastWord in rhymes.keys():
                if (rhymeG not in rhymes[lastWord]):
                    rhymes[lastWord].append(rhymeG) 
            else:
                rhymes[lastWord] = [rhymeG]

    if curLineinPoem < 4 or (curLineinPoem >= 8 and curLineinPoem < 12):
        quatrainWords += words
        curQuatrain += words
        if curLineinPoem % 4 != 3:
            curQuatrain += ['\n']
        elif curLineinPoem == 3:
            quatrains.append(curQuatrain)
            curQuatrain = []
    elif curLineinPoem >= 4 and curLineinPoem < 8:
        voltaWords += words
        curVolta += words
        if curLineinPoem != 7:
            curVolta += ['\n']
    else:
        coupletWords += words
        curCouplet += words
        if curLineinPoem != 13:
            curCouplet += ['\n']
    #stanzaWords += words
    #curStanza += words
    #if curLineinPoem != 13:
    #    curStanza += ['\n']
    curLineinPoem += 1



curLineinPoem = 0
curQuatrain = []
curCouplet = []
curVolta = []
#curStanza = []



# Build lists of quatrains, voltas, and couplets for Spencer's Poems
for i, line in enumerate(spenceLines):
    if line == '\n':
        continue

    words = [x.lower() for x in word_tokenize(line)]

    prevElem = words[0]
    for i, elem in enumerate(words):
        if elem == "is" and prevElem == "'t": # Handle 'tis... unique case
            words[i - 1] = "'tis"
            words.remove(elem)
            elem = words[i - 1]
        elif elem == "'s": # Manually handle apostrophes
            words[i - 1] += "'s"
            words.remove(elem)
            elem = words[i - 1]
        elif elem == "'d": # Manually handle apostrophes
            words[i - 1] += "'d"
            words.remove(elem)
            elem = words[i - 1]
        elif elem in string.punctuation:
            words.remove(elem)
        prevElem = elem

    if len(words) == 1:
        if (curQuatrain != []):
            quatrains.append(curQuatrain)
            voltas.append(curVolta)
            couplets.append(curCouplet)
            #stanzas.append(curStanza)
        curLineinPoem = 0
        curQuatrain = []
        curCouplet = []
        curVolta = []
        #curStanza = []
        continue

    # Build dictionary of rhymes
    if curLineinPoem < 12:
        lastWord = words[-1]
        if (curLineinPoem % 4 == 0):
            rhymeA = lastWord
        if (curLineinPoem % 4 == 2):
            if rhymeA in rhymes.keys():
                if (lastWord not in rhymes[rhymeA]):
                    rhymes[rhymeA].append(lastWord)
            else:
                rhymes[rhymeA] = [lastWord]
            if lastWord in rhymes.keys():
                if (rhymeA not in rhymes[lastWord]):
                    rhymes[lastWord].append(rhymeA) 
            else:
                rhymes[lastWord] = [rhymeA]

        if (curLineinPoem % 4 == 1):
            rhymeB = lastWord
        if (curLineinPoem % 4 == 3):
            if rhymeB in rhymes.keys():
                if (lastWord not in rhymes[rhymeB]):
                    rhymes[rhymeB].append(lastWord)
            else:
                rhymes[rhymeB] = [lastWord]
            if lastWord in rhymes.keys():
                if (rhymeB not in rhymes[lastWord]):
                    rhymes[lastWord].append(rhymeB) 
            else:
                rhymes[lastWord] = [rhymeB]
    else:
        if (curLineinPoem == 12):
            rhymeG = lastWord
        if (curLineinPoem == 13):
            if rhymeG in rhymes.keys():
                if (lastWord not in rhymes[rhymeG]):
                    rhymes[rhymeG].append(lastWord)
            else:
                rhymes[rhymeG] = [lastWord]
            if lastWord in rhymes.keys():
                if (rhymeG not in rhymes[lastWord]):
                    rhymes[lastWord].append(rhymeG) 
            else:
                rhymes[lastWord] = [rhymeG]

    if curLineinPoem < 4 or (curLineinPoem >= 8 and curLineinPoem < 12):
        quatrainWords += words
        curQuatrain += words
        if curLineinPoem % 4 != 3:
            curQuatrain += ['\n']
        elif curLineinPoem == 3:
            quatrains.append(curQuatrain)
            curQuatrain = []
    elif curLineinPoem >= 4 and curLineinPoem < 8:
        voltaWords += words
        curVolta += words
        if curLineinPoem != 7:
            curVolta += ['\n']
    else:
        coupletWords += words
        curCouplet += words
        if curLineinPoem != 13:
            curCouplet += ['\n']
    #stanzaWords += words
    #curStanza += words
    #if curLineinPoem != 13:
    #    curStanza += ['\n']
    curLineinPoem += 1



# Building separate word maps for quatrains, voltas, and couplets
quatrain_word_map = {}
volta_word_map = {}
couplet_word_map = {}
count_words = 0

for word in quatrainWords:
    if word not in quatrain_word_map.keys():
        quatrain_word_map[word] = count_words
        count_words += 1

count_words = 0
for word in voltaWords:
    if word not in volta_word_map.keys():
        volta_word_map[word] = count_words
        count_words += 1

count_words = 0
for word in coupletWords:
    if word not in couplet_word_map.keys():
        couplet_word_map[word] = count_words
        count_words += 1


# Lines are separated by the newLine character, individual 
with open(out_quatrains, 'w') as f: 
    for i in range(len(quatrains)):
        quatrains[i].reverse()
        line = ''
        for elem in quatrains[i]:
            if (elem == '\n'):
                line += elem
            else:
                line += elem + ','
        line += '\n'
        line = line.replace(',\n','\n')
        f.write(line)

print('Dumped Quatrains to ' + out_quatrains + '...')

with open(out_voltas, 'w') as f: 
    for i in range(len(voltas)):
        voltas[i].reverse()
        line = ''
        for elem in voltas[i]:
            if (elem == '\n'):
                line += elem
            else:
                line += elem + ','
        line += '\n'
        line = line.replace(',\n','\n')
        f.write(line)

print('Dumped Voltas to ' + out_voltas + '...')

with open(out_couplets, 'w') as f: 
    for i in range(len(couplets)):
        couplets[i].reverse()
        line = ''
        for elem in couplets[i]:
            if (elem == '\n'):
                line += elem
            else:
                line += elem + ','
        line += '\n'
        line = line.replace(',\n','\n')
        f.write(line)

print('Dumped Couplets to ' + out_couplets + '...')

# Dumped rhymes dictionary in JSON format
with open(out_rhymes, 'w') as f: 
    json.dump(rhymes, f)
print('Dumped rhymes to ' + out_rhymes + '...')

# Dumped quatrain words dictionary in JSON format
with open(out_quatrain_w_to_i, 'w') as f: 
    json.dump(quatrain_word_map, f)
print('Dumped quatrain_word_map to ' + out_quatrain_w_to_i + '...')

# Dumped volta words dictionary in JSON format
with open(out_volta_w_to_i, 'w') as f: 
    json.dump(volta_word_map, f)
print('Dumped volta word map to ' + out_volta_w_to_i + '...')

# Dumped couplet words dictionary in JSON format
with open(out_couplets_w_to_i, 'w') as f: 
    json.dump(couplet_word_map, f)
print('Dumped couplet_word_map to ' + out_couplets_w_to_i + '...')


>>>>>>> origin/master
