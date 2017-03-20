#!/usr/bin/env python3

import sys
import re
from enum import Enum, unique
from sklearn import preprocessing

@unique
class Aspect(Enum):
	PERF = 0
	IMPERF = 1
	BOTH = 2
	UNK = 3


last_letter_count = 4


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
	
	if aspect == Aspect.UNK:
		#sys.stderr.write("Skipping lemma '%s': no aspectual information found.\n" % techlemma)
		continue
	
	
	last_letters = lemma[-last_letter_count:]
	# If len(last_letters) < last_letter_count: pad last_letters with spaces from the left.
	last_letters = " "*(last_letter_count - len(last_letters)) + last_letters
	
	node = {"lemma": lemma,
	        "aspect": aspect,
	        "last_letters": last_letters,
	        "last_letters_onehot": []}
	
	if aspect == Aspect.BOTH:
		# Print the same features twice, once for PERF and once for IMPERF.
		node["aspect"] = Aspect.PERF
		data.append(node)
		
		node = dict(node)
		node["aspect"] = Aspect.IMPERF
		data.append(node)
	else:
		data.append(node)
	
	#print(','.join((lemma,
	                ##str(suffix_id),
	                #str(aspect.value))))

# Transform each of the last letters to one-hot encoding.
#onehot_features = None
for i in range(last_letter_count):
	# Get a column of i-th letters from the data
	letter_list = [item["last_letters"][i] for item in data]
	#sys.stderr.write(str(letter_list))
	
	# Transform this column into one-hot encoding
	onehot_letter = preprocessing.LabelBinarizer().fit_transform(letter_list)
	
	for (node, onehot_current) in zip(data, onehot_letter):
		node["last_letters_onehot"].extend(onehot_current)

# Go over the saved data and print the values.
for item in data:
	print(','.join((item["lemma"],
	                ",".join([str(b) for b in item["last_letters_onehot"]]),
	                str(item["aspect"].value))))
