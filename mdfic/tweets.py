import sys
import re
from itertools import chain

import logging

PARAGRAPH_DELIM = re.compile("\n")
SENTENCE_DELIM = re.compile("[.?!]")
PHRASE_DELIM = re.compile("[,]")
WORD_DELIM = re.compile("\s")
METADATA_DELIM = "\n...\n"


def argmin(L,fn):

    seq = iter(L)
    result = next(seq)
    best = fn(result)
    for x in seq:
        cur = fn(x)
        if cur < best:
            result = x
            best = cur
    return result

def split_paragraphs(text):
    return [p for p in text.split('\n') if p]

def split_tweets(para, delim, maxlen=280):
    """
    If a paragraph is longer than maxlength, split it
    in two parts at the sentence boundary closest to the middle.
    Then recursively split the pieces.
    """
    # print("Splitting '{}'".format(para))
    result = []
    if len(para) <= maxlen:
        result.append(para)
    else:
        # find sentence split closest to the middle
        splits = [m.start() for m in delim.finditer(para)]
        if not splits or min(splits)==len(para)-1:
            # if we can't split it, give up.
            result.append(para)
        else:
            best = argmin(splits, lambda s: abs(len(para)/2 - s))
            #print("best = ",best)
            result.extend(split_tweets(para[:best+1].strip(), delim, maxlen=maxlen))
            result.extend(split_tweets(para[best+1:].strip(), delim, maxlen=maxlen))
    return result



def generate(text,maxlen,appendix=''):
    """
    Generate a set of tweets of length at most maxlen
    from the given text, trying to intelligently break
    the tweets at paragraph and sentence boundaries.
    
    If provided, appendix will be appended to each tweet.

    Generates a sequence of (int,int,str) tuples containing
    the length and content of the given tweet.
    """
    if METADATA_DELIM in text:
        _,text = text.split(METADATA_DELIM)

    # adjust for appendix
    maxlen -= len(appendix)
    # adjst for tweet count '\n###/###'
    maxlen -= 8

    paragraphs = split_tweets(text,PARAGRAPH_DELIM,maxlen=maxlen)
    sentences = list(chain.from_iterable(split_tweets(p,SENTENCE_DELIM,maxlen=maxlen) for p in paragraphs))
    phrases = list(chain.from_iterable(split_tweets(s,PHRASE_DELIM,maxlen=maxlen) for s in sentences))

    tweets = phrases 
    appendix = appendix.replace("\\n","\n")
    for i,t in enumerate(tweets):
        s = "{t}\n{tweet}/{total}{appendix}".format(t=t,appendix=appendix,tweet=i+1, total=len(tweets))
        yield len(s),s
        
