'''

Brief intro:
    This is a simple spell checker on german words with special character. 
    It is specially implemented for replacing course'names having '?' with the right character.
    I got the idea from Peter Novig's blog at http://norvig.com/spell-correct.html

How to use:
    Simply run with : 
        myCorrectStr = correctionStr("Einf?hrung f?r settings?")
    Then myCorrectStr should be:
        'einführung für settings?'

Note: 
    Remember to put the germanwords.p file in the right directory

Created by:
    Ruiming Huang

'''

import re
from collections import Counter
import pickle

WORDS = pickle.load( open( "germanwords.p", "rb" ) )

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'öäüÖÄÜßáóúéÁÓÚÉ'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    return set(replaces)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def correctionWord(word): 
    "Most probable spelling correction for word."
    return max(candidates(word.lower()), key=P)

def correctionStr(string):
    "Correction for a string with multiple words"
    trimstr = re.sub("\s*\(.*\)\s*", "", string)
    strarray = re.findall(r'[A-Z\?]?[a-z\?]+', trimstr)
    for i, substring in enumerate(strarray):
        if "?" in substring:
            strarray[i] = correctionWord(substring)
    resultstr = " ".join(x for x in strarray)        
    return resultstr