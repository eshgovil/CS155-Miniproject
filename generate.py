# Ricky Galliani, David Kawashima, Eshan Govil
# Februray 2017

import random, json
from HMM import *
import numpy as np

# Data from pre-processing
out_quatrains       = 'out_quatrains.csv' 
out_voltas          = 'out_voltas.csv' 
out_couplets        = 'out_couplets.csv'

out_quatrain_w_to_i = 'out_q_w_map.json' 
out_volta_w_to_i    = 'out_v_w_map.json' 
out_couplets_w_to_i = 'out_c_w_map.json' 

out_quatrain_rhymes = 'out_quatrain_rhymes.json'
out_volta_rhymes    = 'out_volta_rhymes.json'
out_couplets_rhymes = 'out_couplets_rhymes.json'

out_quatrain_n_syls = 'out_quatrain_n_syls.json' 
out_volta_n_syls    = 'out_volta_n_syls.json'
out_couplets_n_syls = 'out_couplets_n_syls.json'

# Pull in the quatrain word-to-integer map and integer-to-word map
with open(out_quatrain_w_to_i, 'r') as qr: 
    qrd = qr.read()
    quatrainWordMap = json.loads(qrd)
    quatrainIntMap = dict((int(v),k) for (k,v) in quatrainWordMap.items())

# Pull in the volta word-to-integer map and integer-to-word map
with open(out_volta_w_to_i, 'r') as vr: 
    vrd = vr.read()
    voltaWordMap = json.loads(vrd)
    voltaIntMap = dict((int(v),k) for (k,v) in voltaWordMap.items())

# Pull in the couplet word-to-integer map and integer-to-word map
with open(out_couplets_w_to_i, 'r') as cr: 
    crd = cr.read()
    coupletWordMap = json.loads(crd)
    coupletIntMap = dict((int(v),k) for (k,v) in coupletWordMap.items())

# Pull in the quatrain world-to-syllable map
with open(out_quatrain_n_syls, 'r') as ns:
    nsr = ns.read()
    d = json.loads(nsr)
    quatrain_n_syls = dict([(int(k), int(v)) for (k,v) in d.items()])

# Pull in the volta world-to-syllable map
with open(out_volta_n_syls, 'r') as vs:
    vsr = vs.read()
    d = json.loads(vsr)
    volta_n_syls = dict([(int(k), int(v)) for (k,v) in d.items()])

# Pull in the couplet world-to-syllable map
with open(out_couplets_n_syls, 'r') as cs:
    csr = cs.read()
    d = json.loads(csr)
    couplet_n_syls = dict([(int(k), int(v)) for (k,v) in d.items()])

# Format the quatrain sequences as a list of string lists
quatrainX = []
with open(out_quatrains, 'r') as oq:
    line = oq.readline()
    while line:
        # Remove new lines and convert to a list of strings
        line = line.replace('\n','').replace(',,','').replace('.,','').split(',')
        # Change each word to its corresponding integer
        sequence = []
        for x in line: 
            if x in quatrainWordMap:
                sequence.append(quatrainWordMap[x])
            else: 
                print("Quatrain Key Error: " + str(x))
        
        quatrainX.append(sequence)
        line = oq.readline()

# Format the volta sequences as a list of string lists
voltaX = []
with open(out_voltas, 'r') as ov:
    line = ov.readline()
    while line:
        # Remove new lines and convert to a list of strings
        line = line.replace('\n','').replace(',,','').replace('.,','').split(',')

        # Change each word to its corresponding integer
        sequence = []
        error = False
        for x in line: 
            if x in voltaWordMap:
                sequence.append(voltaWordMap[x])
            else: 
                print("Volta Key Error: " + str(x))
        
        voltaX.append(sequence)
        line = ov.readline()

# Format the couplet sequences as a list of string lists
coupletX = []
with open(out_couplets, 'r') as oc:
    line = oc.readline()
    while line:
        # Remove new lines and convert to a list of strings
        line = line.replace('\n','').replace(',,','').replace('.,','').split(',')

        # Change each word to its corresponding integer
        sequence = []
        for x in line: 
            if x in coupletWordMap:
                sequence.append(coupletWordMap[x])
            else: 
                print("Couplet Key Error: " + str(x))

        # Store couplet sequence
        coupletX.append(sequence)
        line = oc.readline()

# Get the quatrain rhyming dictionary
with open(out_quatrain_rhymes, 'r') as rf:
    rd = rf.read()
    quatrain_rhymes = json.loads(rd)

# Get the volta rhyming dictionary
with open(out_volta_rhymes, 'r') as rf:
    rd = rf.read()
    volta_rhymes = json.loads(rd)

# Get the couplets rhyming dictionary
with open(out_couplets_rhymes, 'r') as rf:
    rd = rf.read()
    couplet_rhymes = json.loads(rd)

def generate_quatrain(quatHMM):
    '''
    Generates a single quatrain. Quatrains follow the ABAB rhyme scheme.

    Uses functions from HMM.py
    '''
    quatrain = ''
    a_rhyme = ''
    b_rhyme = ''
    for i in range(4): 
        if i == 0: # Line A1
            firstWordStr = str(random.choice(list(quatrain_rhymes.keys())))
            firstWordInt = quatrainWordMap[firstWordStr]
            line = quatHMM.generate_emission(firstWordInt, quatrain_n_syls)
            randomRhyme = str(random.choice(quatrain_rhymes[firstWordStr]))
            a_rhyme = quatrainWordMap[randomRhyme]

        elif i == 1: # Line B1
            firstWordStr = str(random.choice(list(quatrain_rhymes.keys())))
            firstWordInt = quatrainWordMap[firstWordStr]
            line = quatHMM.generate_emission(firstWordInt, quatrain_n_syls)
            randomRhyme = str(random.choice(quatrain_rhymes[firstWordStr]))
            b_rhyme = quatrainWordMap[randomRhyme]

        elif i == 2: # Line A2
            line = quatHMM.generate_emission(a_rhyme, quatrain_n_syls)

        elif i == 3: # Line B2
            line = quatHMM.generate_emission(b_rhyme, quatrain_n_syls)

        # Split up the line and reverse the order of the emission
        line = line.split('-')
        line.reverse()

        # Map the integers in the emission back to their corresponding strings
        line = ' '.join([str(quatrainIntMap[int(x)]) for x in line])

        # Capitalize the first letter of each line
        line = line[0].upper() + line[1:]
        line = line.replace(' i ', ' I ')

        # Comma at the end of each line
        quatrain += line + ',\n'

    # End the quatrain with a period
    quatrain += '<>'
    quatrain = quatrain.replace(',\n<>', '.\n')
    return quatrain

def generate_volta(voltHMM):
    '''
    Generates a single volta. voltas follow the ABAB rhyme scheme.
    '''
    volta = ''
    a_rhyme = ''
    b_rhyme = ''
    for i in range(4): 
        if i == 0: # Line A1
            firstWordStr = str(random.choice(list(volta_rhymes.keys())))
            firstWordInt = voltaWordMap[firstWordStr]
            line = voltHMM.generate_emission(firstWordInt, volta_n_syls)
            randomRhyme = str(random.choice(volta_rhymes[firstWordStr]))
            a_rhyme = voltaWordMap[randomRhyme]

        elif i == 1: # Line B1
            firstWordStr = str(random.choice(list(volta_rhymes.keys())))
            firstWordInt = voltaWordMap[firstWordStr]
            line = voltHMM.generate_emission(firstWordInt, volta_n_syls)
            randomRhyme = str(random.choice(volta_rhymes[firstWordStr]))
            b_rhyme = voltaWordMap[randomRhyme]

        elif i == 2: # Line A2
            line = voltHMM.generate_emission(a_rhyme, volta_n_syls)

        elif i == 3: # Line B2
            line = voltHMM.generate_emission(b_rhyme, volta_n_syls)

        # Split up the line and reverse the order of the emission
        line = line.split('-')
        line.reverse()

        # Map the integers in the emission back to their corresponding strings
        line = ' '.join([str(voltaIntMap[int(x)]) for x in line])

        # Capitalize the first letter of each line
        line = line[0].upper() + line[1:]
        line = line.replace(' i ', ' I ')

        # Comma at the end of each line
        volta += line + ',\n'

    # End the volta with a period
    volta += '<>'
    volta = volta.replace(',\n<>', '.\n')
    return volta

def generate_haiku(haikuHMM):
    '''
    Generates a single haiku. Uses volta data.
    '''
    haiku = ''

    for i in range(3): 
        if i == 0: # Line A1
            firstWordStr = str(random.choice(list(voltaWordMap.keys())))
            line = haikuHMM.generate_emission_haiku5(voltaWordMap[firstWordStr], volta_n_syls)

        elif i == 1: # Line B1
            firstWordStr = str(random.choice(list(voltaWordMap.keys())))
            line = haikuHMM.generate_emission_haiku7(voltaWordMap[firstWordStr], volta_n_syls)

        elif i == 2: # Line A2
            firstWordStr = str(random.choice(list(voltaWordMap.keys())))
            line = haikuHMM.generate_emission_haiku5(voltaWordMap[firstWordStr], volta_n_syls)

        # Split up the line and reverse the order of the emission
        line = line.split('-')
        line.reverse()

        # Map the integers in the emission back to their corresponding strings
        line = ' '.join([str(voltaIntMap[int(x)]) for x in line])

        # Capitalize the first letter of each line
        line = line[0].upper() + line[1:]
        line = line.replace(' i ', ' I ')

        # Comma at the end of each line
        haiku += line + ',\n'

    # End the volta with a period
    haiku += '<>'
    haiku = haiku.replace(',\n<>', '.\n')
    return haiku

def generate_couplet(coupletHMM):
    '''
    Generates a single couplet. couplets follow the ABAB rhyme scheme.
    '''
    couplet = ''
    a_rhyme = ''

    for i in range(2): 
        if i == 0: # Line G1
            firstWordStr = str(random.choice(list(couplet_rhymes.keys())))
            firstWordInt = coupletWordMap[firstWordStr]
            line = coupletHMM.generate_emission(firstWordInt, couplet_n_syls)
            randomRhyme = str(random.choice(couplet_rhymes[firstWordStr]))
            a_rhyme = coupletWordMap[randomRhyme]

        elif i == 1: # Line G2
            line = coupletHMM.generate_emission(a_rhyme, couplet_n_syls)

        # Split up the line and reverse the order of the emission
        line = line.split('-')
        line.reverse()

        # Map the integers in the emission back to their corresponding strings
        line = ' '.join([str(coupletIntMap[int(x)]) for x in line])

        # Capitalize the first letter of each line
        line = line[0].upper() + line[1:]
        line = line.replace(' i ', ' I ')

        # Comma at the end of each line
        couplet += line + ',\n'

    # End the couplet with a period
    couplet += '<>'
    couplet = couplet.replace(',\n<>', '.\n')
    return couplet

# Train HMM and generate emissions

# CHOOSE NUMBER OF STATES and ITERATIONS
quatrainStates = 8
quatrainObservations = len(quatrainWordMap)
voltaStates = 8
voltaObservations = len(voltaWordMap)
coupletStates = 8
coupletObservations = len(coupletWordMap)
numiters = 1000

# Train an HMM for the Quatrains
quatHMM = unsupervised_HMM(quatrainX, quatrainStates, quatrainObservations, numiters)

print('')
# Print the transition matrix for quatrains
print("Transition Matrix:")
print('#' * 70)
for i in range(len(quatHMM.A)):
    print(''.join("{:<12.3e}".format(quatHMM.A[i][j]) for j in range(len(quatHMM.A[i]))))
print('')
print('')

# Print top 10 words based on probabilitiy for each state for quatrains
for state in range(5):
    print('List of top 10 words and their corresponding integer assignments and probabilities')
    print('for Hidden state ' + str(state))
    maxprobwords = ['' for i in range(10)]
    maxprobints = [0. for i in range(10)]
    maxprobs = [0. for i in range(10)]
    maxprobwords[0] = str(quatrainIntMap[np.argmax(quatHMM.O[state])])
    maxprobints[0] = np.argmax(quatHMM.O[state])
    maxprobs[0] = quatHMM.O[state][maxprobints[0]]
    for z in range(9):
        maxprobwords[z+1] = quatHMM.O[state][0]
        maxprobints[z+1] = 0
        maxprobs[z+1] = quatHMM.O[state][maxprobints[z+1]]
        for i in range(quatHMM.D):
            if quatHMM.O[state][i] >= quatHMM.O[state][maxprobints[z+1]] \
            and quatHMM.O[state][i] < quatHMM.O[state][maxprobints[z]]:
                maxprobwords[z+1] = str(quatrainIntMap[i])
                maxprobints[z+1] = i
                maxprobs[z+1] = quatHMM.O[state][maxprobints[z+1]]
    print(maxprobwords)
    print(maxprobints)
    print(maxprobs)
    print('\n')

quatrain_1 = generate_quatrain(quatHMM)
quatrain_2 = generate_quatrain(quatHMM)

print("\n")
print(str(quatrain_1))
print(str(quatrain_2))

# Train an HMM for the Voltas
voltHMM = unsupervised_HMM(voltaX, voltaStates, voltaObservations, numiters)
volta_1 = generate_volta(voltHMM)
volta_2 = generate_volta(voltHMM)

print("\n")
print(str(volta_1))
print(str(volta_2))

# Train an HMM for the Coupletas
coupletHMM = unsupervised_HMM(coupletX, coupletStates, coupletObservations, numiters)
couplet_1 = generate_couplet(coupletHMM)
couplet_2 = generate_couplet(coupletHMM)

print("\n")
print(str(couplet_1))
print(str(couplet_2))

# Generate Haiku
haikuHMM = unsupervised_HMM(voltaX, voltaStates, voltaObservations, numiters)
haiku_1 = generate_haiku(haikuHMM)

print('\n')
print(str(haiku_1))