# Ricky Galliani, David Kawashima, Eshan Govil
# Februray 2017

import random, json
from HMM import *

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
    copuletIntMap = dict((int(v),k) for (k,v) in coupletWordMap.items())

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
    couplets_rhymes = json.loads(rd)

quatrainStates = 30
quatrainObservations = len(quatrainWordMap)
voltaStates = 26
voltaObservations = len(voltaWordMap)
coupletStates = 24
coupletObservations = len(coupletWordMap)

def generate_quatrain(quatHMM):
    '''
    Generates a single quatrain. Quatrains follow the ABAB rhyme scheme.
    '''
    quatrain = ''
    a_rhyme = ''
    b_rhyme = ''
    for i in range(4): 
        if i == 0: # Line A1
            firstWordStr = str(random.choice(quatrain_rhymes.keys()))
            firstWordInt = quatrainWordMap[firstWordStr]
            line = quatHMM.generate_emission(firstWordInt, quatrain_n_syls)
            randomRhyme = str(random.choice(quatrain_rhymes[firstWordStr]))
            a_rhyme = quatrainWordMap[randomRhyme]

        elif i == 1: # Line B1
            firstWordStr = str(random.choice(quatrain_rhymes.keys()))
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

# Train an HMM for the Quatrains
quatHMM = unsupervised_HMM(quatrainX, quatrainStates, quatrainObservations, 1)
quatrain_1 = generate_quatrain(quatHMM)
quatrain_2 = generate_quatrain(quatHMM)

print("\n")
print(str(quatrain_1))
print(str(quatrain_2))
