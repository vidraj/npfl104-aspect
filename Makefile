SHELL := /bin/bash
.PHONY: all download prepare split visualize show clean

DERINET_FILE := derinet-1-4b1.tsv

# TODO
all: split

download: $(DERINET_FILE)
prepare: features.csv
split: train.txt test.txt
visualize: # TODO
	# Prepare PDF/PNG plots describing the training data, include a least-squares fit of something.
show: # TODO
	# Just run your favourite image viewer on the files created by make visualize.
	# TODO

$(DERINET_FILE):
	# Download the dataset from whatever source.
	curl --compressed --output "$@" "https://jonys.cz/derinet/search/$(DERINET_FILE)"

features.csv: verbs.txt get-features.py
	# Prepare the downloaded dataset, reformatting as needed, cleaning as needed. Produce:
	#  Line-oriented CSV
	#  The last item on each line is the expected answer.
	
	# Get some features from the verbs. Also creates "header.txt"
	./get-features.py < "$<" > "$@"

features-with-header.csv: features.csv
	cp header.txt "$@"
	cat "$<" >> "$@"

verbs.txt: $(DERINET_FILE)
	# Retrieve only lexemes corresponding to verbs and cut out just the techlemma
	grep '	V	[0-9]*$$' "$<" | cut -f3 > "$@"

features-shuffled.csv: features.csv get-seeded-random.sh
	# Shuffle the dataset with a seeded chaotic process
	shuf --random-source=<(./get-seeded-random.sh 12345) "$<" > "$@"

test.txt: features-shuffled.csv
	# Take the first 1/8 of the shuffled file, delete the labels.
	head -n $$(echo `wc -l < "$<"` / 8 |bc) "$<" |cut -d, -f2- > "$@"
	# Put the labels in a separate file.
	head -n $$(echo `wc -l < "$<"` / 8 |bc) "$<" |cut -d, -f1 > test-labels.txt

train.txt: features-shuffled.csv test.txt
	# Take whatever is not in test.txt, delete the labels.
	tail -n +$$(echo `wc -l < test.txt` + 1 |bc) "$<" |cut -d, -f2- > "$@"
	# Put the labels in a separate file.
	tail -n +$$(echo `wc -l < test.txt` + 1 |bc) "$<" |cut -d, -f1 > train-labels.txt


correlations.png: features-with-header.csv draw-correlation.py
	# Draw a matrix of correlations between selected features and the output class.
	./draw-correlation.py "$<"





clean:
# 	rm -f derinet-*.tsv
	rm -f verbs.txt features.csv features-shuffled.csv train.txt test.txt train-labels.txt test-labels.txt header.txt
