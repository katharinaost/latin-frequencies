# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 08:10:04 2023

@author: Katharina Ost
"""

import argparse
import csv
import xlsxwriter
from collections import Counter
from pathlib import Path

import spacy
from spacy.lang.la import LatinDefaults

#define and process command line arguments
parser = argparse.ArgumentParser(description='Count lemmata.')
parser.add_argument("input", action='store', type = str,
                    help='Path to file or folder containing Latin text(s)')
parser.add_argument('--stopwords', action='store', type = str,
                    help='Path to stop word list (one word per line)')
parser.add_argument('--output', action='store', type = str,
                    help='Store output in file')
parser.add_argument('--output_type', action='store', type = str,
                    choices = ['excel', 'csv'], default ='csv',
                    help='Store output in file')
parser.add_argument('--coverage', action='store', type = int,
                    help='Achieve x% of vocabulary coverage')
parser.add_argument('--top', action='store', type = int,
                    help='Get the top x most frequent words')
args = parser.parse_args()

if not Path(args.input).exists():
    print("The input file/folder does not exist. Exiting.")
    raise SystemExit(1)
    
ner_text = list()

if Path(args.input).is_file():
    ner_text.append(open(args.input).read())
elif Path(args.input).is_dir():
    for file in Path(args.input).iterdir():
        if file.is_file(): #ignore subdirectories
            ner_text.append(open(file).read())

#load custom stop word list, if none is specified the spacy defaults are used
stopwords = args.stopwords
if stopwords != None:
    LatinDefaults.stop_words = set()
    stopword_file = open(stopwords)
    for line in stopword_file:
        LatinDefaults.stop_words.add(line.rstrip())
    
#load language model
nlp = spacy.load('la_core_web_lg')

#apply nlp pipeline
docs = list(nlp.pipe(ner_text))

#get lemmata
lemmata = list()
for doc in docs:
    for token in doc:
        if not token.is_stop and not token.is_punct:
            lemmata.append((token.lemma_, token.pos_))
        
#count word frequencies
word_frequencies = Counter(lemmata)

common_words = list()

#do we need to achive a certain coverage %?
if args.coverage != None:
    total = sum(word_frequencies.values())   #count across all lemmata
    counter = 0                             #running count
    lemma_coverage = 0
    for word in word_frequencies.most_common(): #sort word_frequencies
        common_words.append(word)
        counter += word[1]
        lemma_coverage = counter / total
        if round(lemma_coverage*100) >= args.coverage:
            break
#... or just count the top x?
else:
    #if args.top is None, all lemmata are returned
    common_words = word_frequencies.most_common(args.top)

#store the output
if args.output != None:
    match(args.output_type):
        #CSV Export (default)
        case 'csv':
            with open(args.output, 'w', encoding='UTF8', newline='') as file:
                header = ['lemma', 'pos', 'count']
                writer = csv.writer(file, dialect='excel')
                writer.writerow(header)
                for word in common_words:
                    writer.writerow([word[0][0], word [0][1], word[1]])
                
        #Excel export
        case 'excel':        
            workbook = xlsxwriter.Workbook('output.xlsx')
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': True})
            row = 1
            col = 0
            
            #write header
            worksheet.write('A1', 'Lemma', bold)
            worksheet.write('B1', 'POS', bold)
            worksheet.write('C1', 'Count', bold)
             
            #write data
            for word in common_words:
                worksheet.write(row, col, word[0][0])     #lemma
                worksheet.write(row, col + 1, word[0][1]) #pos
                worksheet.write(row, col + 2, word[1])    #count
                row += 1
            workbook.close()
            
#... or print the output to stdout
else:
    print('The following stop words were used: ', end = '')
    for word in nlp.Defaults.stop_words:
        print(word, end = ' ')
    print ('')
    
    print('lemma, pos, count')
    for word in common_words:
        print(word[0][0] +', ' + word [0][1] + ', ' + str(word[1]))

#give us some coverage information:
count = 0
for word in common_words:
    count += word[1]
lemma_coverage = count / sum(word_frequencies.values())
print("The top " + str(len(common_words)) + " lemmata cover " +
      str(round(lemma_coverage*100)) + "% of vocabulary use in the selected" +
      " corpus (excluding stop words)")

