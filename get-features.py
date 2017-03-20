#!/usr/bin/env python3

import sys
import re
from enum import Enum, unique

@unique
class Aspect(Enum):
    PERF = 0
    IMPERF = 1
    BOTH = 2
    UNK = 3

# Split the techlemma into basic groups.
# See https://ufal.mff.cuni.cz/pdt2.0/doc/manuals/en/m-layer/html/ch02s01.html for explanations.
split_lemma_suffixes = re.compile("^([^_`-]+)(-\d+)?(`[^_]+)?(_.*)?$")
data = []

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
    
    if aspect not in (Aspect.IMPERF, Aspect.PERF):
        # TODO if Aspect.BOTH, should we print the same features twice, once for IMPERF and once for PERF?
        #sys.stderr.write("Skipping lemma '%s': no aspectual information found.\n" % techlemma)
        continue
    
    node = {"lemma": lemma,
            "aspect": aspect}
    
    data.append(node)
    
    #print(','.join((lemma,
                    ##str(suffix_id),
                    #str(aspect.value))))

# Go over the saved data and print the values.
for item in data:
    print(','.join((item["lemma"],
                    str(item["aspect"].value))))
