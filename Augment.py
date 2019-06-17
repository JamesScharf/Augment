'''
Created by James A. Scharf on 6/15/19

Goal: Create a program that can generate fake sentence from inputted ones

It's designed to be effective for data used in a Bag of Words model

Methods:
    1. Randomly select N number of words to replace with random synonyms
    2. Randomly delete a word
    3. Delete a word and replace with its definition
'''
import random

from textblob import Word
from textblob.wordnet import VERB
from textblob.wordnet import NOUN
from textblob.wordnet import ADJ
from textblob.wordnet import ADV
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
#unfortunately the pos tags do not map perfectly to types
posMappings = {
    "JJ": ADJ,
    "JJR" : ADJ,
    "JJS" : ADJ,
    "NNS" : NOUN,
    "NN" : NOUN,
    "NNP" : NOUN,
    "NNPS" : NOUN,
    "RB" : ADV,
    "RBR" : ADV,
    "RBS" : ADV,
    "VB" : VERB,
    "VBZ" : VERB,
    "VBP" : VERB,
    "VBP" : VERB,
    "VBD" : VERB,
    "VBN" : VERB
}



def getRandomSyn(origWord, pos):
    '''
    Given a word (object) and its part of
    speech, select a random synonym and
    spit it out
    '''
    synsets = Word(origWord).get_synsets(pos=pos)
    #now get a list of likely alternatives

    numSynsets = len(synsets)
    #select random synset
    #if numSynsets >= 4:
    #    synset = synsets[random.randint(1, 3)]
    if numSynsets == 1:
        synset = synsets[0]
    elif numSynsets == 0:
        return origWord
    else:
        synset = synsets[random.randint(1, numSynsets - 1)]

    lems = synset.lemmas()
    numLems = len(lems)
    if numLems == 1:
        return lems[0].name()
    result = lems[random.randint(0, numLems - 1)].name()
    if result == origWord:
        return getRandomSyn(origWord, pos)
    return result.replace("_", " ")


def synonymizeRandomWords(document):
    '''
    Given a string, this program
    will replace random numbers of words
    with their synonyms
    '''

    document = document.lower()
    text = TextBlob(document)
    newDoc = document.split()

    numWords = len(newDoc)
    toReplace = random.randint(1, numWords)

    replaced = 0

    while replaced < toReplace:
        locToChange = random.randint(0, numWords - 1)
        if text.tags[locToChange][1] in posMappings:
            newDoc[locToChange] = getRandomSyn(newDoc[locToChange], posMappings[text.tags[locToChange][1]])
            replaced += 1

    return " ".join(newDoc)

def deleteRandomWord(document):
    '''
    Given a document, remove a random word
    '''
    splitDoc = document.split()
    toRemove = random.randint(0, len(splitDoc) - 1)
    del splitDoc[toRemove]
    return " ".join(splitDoc)

def replaceWithDefinition(document):
    '''
    Replace random number of words with
    their definitions
    '''
    splitDoc = document.split()
    text = TextBlob(document)
    toRemove = random.randint(1, len(splitDoc) - 1)
    numWords = len(splitDoc)
    replaced = 0
    while replaced < toRemove:
        locToChange = random.randint(0, numWords - 1)
        currWord = Word(splitDoc[locToChange])
        
        if text.tags[locToChange][1] in posMappings:
            pos = posMappings[text.tags[locToChange][1]]
            syns = currWord.get_synsets(pos=pos)
            if len(syns) > 0:
                defin = syns[0].definition()
                if numWords > len(defin):
                    #only change it if there's a decent difference
                    splitDoc[locToChange] = defin
        replaced += 1
    return " ".join(splitDoc)

def augment(document, replaceSyns, delWord, replaceDef):
    '''
    Perform an augmentation on a given sentence

    replaceSyns = True/False whether to replace words with synonyms
    delWord = True/False whether to delete a random word
    replaceDef = True/False whether to replace a word with a definition
    '''

    #our result
    augmentedSentences = [document]
    if replaceSyns == True:
        augmentedSentences.append(synonymizeRandomWords(document))

    if delWord == True:
        augmentedSentences.append(deleteRandomWord(document))
    if replaceWithDefinition == True:
        augmentedSentences.append(replaceDef(document))

    return augmentedSentences

def batchAugment(documents, replaceSyns, delWord, replaceDef):
    '''
    Run batch augmentation on a list

    replaceSyns = True/False whether to replace words with synonyms
    delWord = True/False whether to delete a random word
    replaceDef = True/False whether to replace a word with a definition
    '''

    augmentedResult = []
    augmentedResult.extend(documents)
    for doc in documents:
        augmentedResult.extend(augment(doc, replaceSyns, delWord, replaceDef))
    
    return augmentedResult