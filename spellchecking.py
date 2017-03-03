import re
from collections import Counter

def words(text): return re.findall(r'\w+', text)

#define in class so only called once 
class ALLWORDS: 
    W = Counter(words(open('big.txt', 'r').read()))

#find probability of word from occurances of word in large text file
def Probability(word): 
    counter = ALLWORDS()
    WORDS = counter.W
    return WORDS[word]

#all words reachable by 1 or 2 edits 
def candidates(word, W): 
    return (known([word], W) or known(edits1(word), W) or known(edits2(word),W) or [word])

#all know words from text
def known(words, W): 
    return set(w for w in words if w in W)

#all words reachable by 1 modification
def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

#all words reachable by 2 modifications 
def edits2(word): 
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))
    
#best option of corrected word, due to probability key 
def spellcheck(word, W):  
    if known([word],W):
        return word 
    return max(candidates(word,W), key=Probability)

#spellcheck all words in text 
def checkText(input): 
    counter = ALLWORDS()
    WORDS = counter.W
    text = re.sub("[^a-zA-Z]", " ", input).split()
    output = ""
    for w in text: 
        w = spellcheck(w, WORDS)
        output+=w
        output+=" "
    return output
