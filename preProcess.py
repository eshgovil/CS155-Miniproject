import sys, time, pandas as pd
import nltk
from nltk.corpus import cmudict
import nltk.data
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder
import json


#nltk.download()
d = cmudict.dict()

count_problems = 0
# taken from somewhere
def nsyl(word):
    if word.lower() not in d.keys():
        return 11
    return max([len([y for y in x if y[-1].isdigit()]) for x in d[word.lower()]])

quatrainWords = []
coupletWords = []
voltaWords = []

quatrains = []
couplets = []
voltas = []


q_rhymes = {}
v_rhymes = {}
c_rhymes = {}

f_shake = open('./project2data/shakespeare.txt')
f_spence = open('./project2data/spenser.txt')


out_quatrains= 'out_quatrains.csv' 
out_voltas = 'out_voltas.csv' 
out_couplets = 'out_couplets.csv'
out_rhymes = 'out_rhymes.json'

out_q_rhymes = 'out_quatrain_rhymes.json'
out_v_rhymes = 'out_volta_rhymes.json'
out_c_rhymes = 'out_couplets_rhymes.json'

out_quatrain_w_to_i = 'out_q_w_map.json' 
out_volta_w_to_i = 'out_v_w_map.json' 
out_couplets_w_to_i = 'out_c_w_map.json'

out_quatrain_i_to_nsyl = 'out_quatrain_n_syls.json' 
out_volta_i_to_nsyl = 'out_volta_n_syls.json' 
out_couplets_i_to_nsyl= 'out_couplets_n_syls.json'   

shakeLines = f_shake.readlines()
spenceLines = f_spence.readlines()

curLineinPoem = 0
curQuatrain = []
curCouplet = []
curVolta = []

rhymeA = "";
rhymeB = "";
rhymeG = "";

# Build lists of quatrains, voltas, and couplets for Shakespeare's Poems
for i, line in enumerate(shakeLines):
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
        if elem in string.punctuation:
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
    lastWord = words[-1]
    if curLineinPoem < 4 or (curLineinPoem >= 8 and curLineinPoem < 12):
    
        if (curLineinPoem % 4 == 0):
            rhymeA = lastWord 
        if (curLineinPoem % 4 == 2):
            if nsyl(lastWord) != 11 and nsyl(rhymeA) != 11:
                if rhymeA in q_rhymes.keys():
                    if (lastWord  not in q_rhymes[rhymeA]):
                        q_rhymes[rhymeA].append(lastWord)
                else:
                    q_rhymes[rhymeA] = [lastWord]
                if lastWord in q_rhymes.keys():
                    if (rhymeA not in q_rhymes[lastWord]):
                        q_rhymes[lastWord].append(rhymeA) 
                else:
                    q_rhymes[lastWord] = [rhymeA]

        if (curLineinPoem % 4 == 1):
            rhymeB = lastWord
        if (curLineinPoem % 4 == 3):
            if nsyl(lastWord) != 11 and nsyl(rhymeB) != 11:
                if rhymeB in q_rhymes.keys():
                    if (lastWord not in q_rhymes[rhymeB]):
                        q_rhymes[rhymeB].append(lastWord)
                else:
                    q_rhymes[rhymeB] = [lastWord]
                if lastWord in q_rhymes.keys():
                    if (rhymeB not in q_rhymes[lastWord]):
                        q_rhymes[lastWord].append(rhymeB) 
                else:
                    q_rhymes[lastWord] = [rhymeB]

        quatrainWords += words
        curQuatrain += words
        if curLineinPoem % 4 != 3:
            curQuatrain += ['\n']
        elif curLineinPoem == 3:
            quatrains.append(curQuatrain)
            curQuatrain = []
    elif curLineinPoem >= 4 and curLineinPoem < 8:
        
        if (curLineinPoem % 4 == 0):
            rhymeA = lastWord 
        if (curLineinPoem % 4 == 2):
            if nsyl(lastWord) != 11 and nsyl(rhymeA) != 11:
                if rhymeA in v_rhymes.keys():
                    if (lastWord  not in v_rhymes[rhymeA]):
                        v_rhymes[rhymeA].append(lastWord)
                else:
                    v_rhymes[rhymeA] = [lastWord]
                if lastWord in v_rhymes.keys():
                    if (rhymeA not in v_rhymes[lastWord]):
                        v_rhymes[lastWord].append(rhymeA) 
                else:
                    v_rhymes[lastWord] = [rhymeA]

        if (curLineinPoem % 4 == 1):
            rhymeB = lastWord
        if (curLineinPoem % 4 == 3):
            if nsyl(lastWord) != 11 and nsyl(rhymeB) != 11:
                if rhymeB in v_rhymes.keys():
                    if (lastWord not in v_rhymes[rhymeB]):
                        v_rhymes[rhymeB].append(lastWord)
                else:
                    v_rhymes[rhymeB] = [lastWord]
                if lastWord in v_rhymes.keys():
                    if (rhymeB not in v_rhymes[lastWord]):
                        v_rhymes[lastWord].append(rhymeB) 
                else:
                    v_rhymes[lastWord] = [rhymeB]

        voltaWords += words
        curVolta += words
        if curLineinPoem != 7:
            curVolta += ['\n']
    else:
        if (curLineinPoem == 12):
            rhymeG = lastWord
        if (curLineinPoem == 13):
            if nsyl(lastWord) != 11 and nsyl(rhymeG) != 11:
                if rhymeG in c_rhymes.keys():
                    if (lastWord not in c_rhymes[rhymeG]):
                        c_rhymes[rhymeG].append(lastWord)
                else:
                    c_rhymes[rhymeG] = [lastWord]
                if lastWord in c_rhymes.keys():
                    if (rhymeG not in c_rhymes[lastWord]):
                        c_rhymes[lastWord].append(rhymeG) 
                else:
                    c_rhymes[lastWord] = [rhymeG]

        coupletWords += words
        curCouplet += words
        if curLineinPoem != 13:
            curCouplet += ['\n']
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
        elif elem == "":
            words.remove(elem)
        elif elem == "'s": # Manually handle apostrophes
            words[i - 1] += "'s"
            words.remove(elem)
            elem = words[i - 1]
        elif elem == "'d": # Manually handle apostrophes
            words[i - 1] += "'d"
            words.remove(elem)
            elem = words[i - 1]
        if elem in string.punctuation:
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
    lastWord = words[-1]
    if curLineinPoem < 4 or (curLineinPoem >= 8 and curLineinPoem < 12):
        if (curLineinPoem % 4 == 0):
            rhymeA = lastWord 
        if (curLineinPoem % 4 == 2):
            if nsyl(lastWord) != 11 and nsyl(rhymeA) != 11:
                if rhymeA in q_rhymes.keys():
                    if (lastWord  not in q_rhymes[rhymeA]):
                        q_rhymes[rhymeA].append(lastWord)
                else:
                    q_rhymes[rhymeA] = [lastWord]
                if lastWord in q_rhymes.keys():
                    if (rhymeA not in q_rhymes[lastWord]):
                        q_rhymes[lastWord].append(rhymeA) 
                else:
                    q_rhymes[lastWord] = [rhymeA]

        if (curLineinPoem % 4 == 1):
            rhymeB = lastWord
        if (curLineinPoem % 4 == 3):
            if nsyl(lastWord) != 11 and nsyl(rhymeB) != 11:
                if rhymeB in q_rhymes.keys():
                    if (lastWord not in q_rhymes[rhymeB]):
                        q_rhymes[rhymeB].append(lastWord)
                else:
                    q_rhymes[rhymeB] = [lastWord]
                if lastWord in q_rhymes.keys():
                    if (rhymeB not in q_rhymes[lastWord]):
                        q_rhymes[lastWord].append(rhymeB) 
                else:
                    q_rhymes[lastWord] = [rhymeB]

        quatrainWords += words
        curQuatrain += words
        if curLineinPoem % 4 != 3:
            curQuatrain += ['\n']
        elif curLineinPoem == 3:
            quatrains.append(curQuatrain)
            curQuatrain = []
    elif curLineinPoem >= 4 and curLineinPoem < 8:
        if (curLineinPoem % 4 == 0):
            rhymeA = lastWord 
        if (curLineinPoem % 4 == 2):
            if nsyl(lastWord) != 11 and nsyl(rhymeA) != 11:
                if rhymeA in v_rhymes.keys():
                    if (lastWord  not in v_rhymes[rhymeA]):
                        v_rhymes[rhymeA].append(lastWord)
                else:
                    v_rhymes[rhymeA] = [lastWord]
                if lastWord in v_rhymes.keys():
                    if (rhymeA not in v_rhymes[lastWord]):
                        v_rhymes[lastWord].append(rhymeA) 
                else:
                    v_rhymes[lastWord] = [rhymeA]

        if (curLineinPoem % 4 == 1):
            rhymeB = lastWord
        if (curLineinPoem % 4 == 3):
            if nsyl(lastWord) != 11 and nsyl(rhymeB) != 11:
                if rhymeB in v_rhymes.keys():
                    if (lastWord not in v_rhymes[rhymeB]):
                        v_rhymes[rhymeB].append(lastWord)
                else:
                    v_rhymes[rhymeB] = [lastWord]
                if lastWord in v_rhymes.keys():
                    if (rhymeB not in v_rhymes[lastWord]):
                        v_rhymes[lastWord].append(rhymeB) 
                else:
                    v_rhymes[lastWord] = [rhymeB]

        voltaWords += words
        curVolta += words
        if curLineinPoem != 7:
            curVolta += ['\n']
    else:
        if (curLineinPoem == 12):
            rhymeG = lastWord
        if (curLineinPoem == 13):
            if nsyl(lastWord) != 11 and nsyl(rhymeG) != 11:
                if rhymeG in c_rhymes.keys():
                    if (lastWord not in c_rhymes[rhymeG]):
                        c_rhymes[rhymeG].append(lastWord)
                else:
                    c_rhymes[rhymeG] = [lastWord]
                if lastWord in c_rhymes.keys():
                    if (rhymeG not in c_rhymes[lastWord]):
                        c_rhymes[lastWord].append(rhymeG) 
                else:
                    c_rhymes[lastWord] = [rhymeG]

        coupletWords += words
        curCouplet += words
        if curLineinPoem != 13:
            curCouplet += ['\n']
    curLineinPoem += 1



# Building separate word maps for quatrains, voltas, and couplets
quatrain_word_map = {}
volta_word_map = {}
couplet_word_map = {}
quatrain_n_syls_map = {}
volta_n_syls_map = {}
couplets_n_syls_map = {}

count_words = 0

for word in quatrainWords:
    if word not in quatrain_word_map.keys():
        quatrain_word_map[word] = count_words
        count_words += 1
        if word not in quatrain_n_syls_map.keys():
            if nsyl(word) == 11:
                count_problems += 1
            quatrain_n_syls_map[count_words - 1] = nsyl(word)

count_words = 0
for word in voltaWords:
    if word not in volta_word_map.keys():
        volta_word_map[word] = count_words
        count_words += 1
        if word not in volta_n_syls_map.keys():
            if nsyl(word) == 11:
                count_problems += 1
            volta_n_syls_map[count_words - 1] = nsyl(word)

count_words = 0
for word in coupletWords:
    if word not in couplet_word_map.keys():
        couplet_word_map[word] = count_words
        count_words += 1
        if word not in couplets_n_syls_map.keys():
            if nsyl(word) == 11:
                count_problems += 1
            couplets_n_syls_map[count_words - 1] = nsyl(word)




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

# Dumped quatrain number of syllables dictionary in JSON format
with open(out_quatrain_i_to_nsyl, 'w') as f: 
    json.dump(quatrain_n_syls_map, f)
print('Dumped quatrain_n_syls_map to ' + out_quatrain_i_to_nsyl + '...')

# Dumped volta number of syllables dictionary in JSON format
with open(out_volta_i_to_nsyl, 'w') as f: 
    json.dump(volta_n_syls_map, f)
print('Dumped volta_n_syls_map to ' + out_volta_i_to_nsyl + '...')

# Dumped couplet words dictionary in JSON format
with open(out_couplets_i_to_nsyl, 'w') as f: 
    json.dump(couplets_n_syls_map, f)
print('Dumped couplets_n_syls_map to ' + out_couplets_i_to_nsyl + '...')

# Dumped quatrain rhyme dictionary in JSON format
with open(out_q_rhymes, 'w') as f: 
    json.dump(q_rhymes, f)
print('Dumped quatrain_rhymes to ' + out_q_rhymes + '...')

# Dumped volta rhyme dictionary in JSON format
with open(out_v_rhymes, 'w') as f: 
    json.dump(v_rhymes, f)
print('Dumped volta_rhymes to ' + out_v_rhymes + '...')

# Dumped couplet rhyme dictionary in JSON format
with open(out_c_rhymes, 'w') as f: 
    json.dump(c_rhymes, f)
print('Dumped couplets_rhymes to ' + out_c_rhymes + '...')
