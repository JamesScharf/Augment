# Augment

This is a very simple program that creates augmented, or fake, text data. It works best on
large documents.


## Useful functions:

Before using, you must `import Augment`

* augment:
    Perform an augmentation on a given sentence
    
    Arguments:
    
    document = one string
    replaceSyns = True/False whether to replace words with synonyms
    delWord = True/False whether to delete a random word
    replaceDef = True/False whether to replace a word with a definition

* batchAugment:
    Perform an augmentation on a given list of sentences
    
    Arguments:
    
    documents = a list of strings
    replaceSyns = True/False whether to replace words with synonyms
    delWord = True/False whether to delete a random word
    replaceDef = True/False whether to replace a word with a definition