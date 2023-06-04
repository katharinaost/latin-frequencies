# latin-frequencies

Simple script that generates word frequency lists for Latin texts

## Prerequisites
spaCy with the [LatinCy](https://huggingface.co/latincy) pipeline (la_core_web_lg model), XlsxWriter 

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
 
 
