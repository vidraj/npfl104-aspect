#!/usr/bin/env python3

import sys
import re
from enum import Enum, unique
from collections import defaultdict
from time import clock

import numpy as np

@unique
class Aspect(Enum):
    PERF = 0
    IMPERF = 1
    BOTH = 2
    UNK = 3

# Split the techlemma into basic groups.
# See https://ufal.mff.cuni.cz/pdt2.0/doc/manuals/en/m-layer/html/ch02s01.html for explanations.
split_lemma_suffixes = re.compile("^([^_`-]+)(-\d+)?(`[^_]+)?(_.*)?$")
max_n = 4
min_freq = 1000
header_fname = 'header.txt'

def make_ngrams(word, max_n):
    ngram_list = []
    word = '_' + word + '_'
    for i in range(2, max_n + 1):
        ngram_list.extend([word[j:j+i] for j in range(0, len(word) - i + 1)])
    return tuple(ngram_list)

def vectorize(item, feature_list):
    return np.in1d(feature_list, item[:-2]).astype(int)

if __name__ == "__main__":
    ngrammed_data = []
    feature_counter = defaultdict(int)
    btime = clock()

    # Go over the input, retrieving and saving features for each line.
    for techlemma in sys.stdin:
        techlemma = techlemma.rstrip()
        match = split_lemma_suffixes.match(techlemma)
        (lemma, homonym_number, explanation, technical_suffixes) = match.groups(default='')
    
        if ("_:T" in technical_suffixes) and ("_:W" in technical_suffixes):
            aspect = Aspect.BOTH
        elif "_:T" in technical_suffixes:
            aspect = Aspect.IMPERF
        elif "_:W" in technical_suffixes:
            aspect = Aspect.PERF
        else:
            aspect = Aspect.UNK
    
        if aspect in (Aspect.IMPERF, Aspect.PERF):
            ngrams = make_ngrams(lemma, max_n)
            for ngram in ngrams:
                feature_counter[ngram] += 1
            ngrammed_data.append(make_ngrams(lemma, max_n) + (lemma, str(aspect.value)))

    ngrammed_data = np.asarray(ngrammed_data)

    feature_counter = {feature: feature_counter[feature]
                          for feature in feature_counter
                              if feature_counter[feature] >= min_freq}

    print('{} features after cutoff by min frequency of {}'.format(
          len(feature_counter), min_freq), file=sys.stderr)

    feature_list = np.asarray(sorted(feature_counter, key=feature_counter.get, reverse=True))

    with open(header_fname, 'w', encoding='utf-8') as header_file: 
        print('lemma', end=',', file=header_file)
        print(*feature_list, sep=',', end=',', file=header_file)
        print('class', file=header_file)

    for item in ngrammed_data:
        print(item[-2], end=',')
        print(*vectorize(item, feature_list), sep=',', end=',')
        print(item[-1])

    print('Finished in {:.2f}'.format(clock() - btime), file=sys.stderr)
