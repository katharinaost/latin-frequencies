# latin-frequencies

Simple script that generates word frequency lists for Latin texts

## Prerequisites
[spaCy](https://spacy.io/) with the la_core_web_lg [LatinCy](https://huggingface.co/latincy) pipeline, [XlsxWriter](https://github.com/jmcnamara/XlsxWriter) 

 ```sh
pip install -U XlsxWriter
pip install -U pip setuptools wheel
pip install -U spacy
pip install https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl
```


## Usage
Example:
 ```sh
   python frequency.py --stopwords=stopwords.txt --coverage=80 --output_type=excel --output=output.xlsx documents
 ```
 Collects lemma frequencies for all (plaintext) files in the "documents" directory, using the supplied stop-word file. Returns the top lemmata until at least 80% coverage are achieved in an excel file.
 
![Excel output](https://i.imgur.com/rYAt8Ni.png)
 
 ### Arguments
* filename/folder: Path of a file or folder to process (obligatory).
* __--stopwords__=filename: Path of a textfile containing a list of stop words (one entry per line). If not supplied, the default stop-word list of the spaCy model is used. Point this to an empty file, if you don't want to use any stop words.
* __--output__=filename: Where to store the output. If not supplied, output will be printed to stdout.
* __--output_type__=excel/csv: What kind of output to generate. Only applies if --output is specified, defaults to "csv".
* __--coverage__=n: Lists the most common lemmata in descending order until at least "n" percent of vocabulary coverage is achieved. Takes precedence over --top.
* __--top__=n: Lists the "n" most frequent lemmata. If neither --coverage nor --top are supplied, all lemmata are listed. 
