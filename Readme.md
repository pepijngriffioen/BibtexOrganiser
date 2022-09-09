# Bib processor
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

I created this bibtex parser to help me with some problems I had with the Mendeley online export function. The main problem is the missing of citation keys for some entries. First I added them manually, but as I had to recreate the bib file quite often, this was a waste of time. To make this process more easy I wrote this script. 

I hope Mendeley fixes this issue in the future, but for now I got you covered! I you feel the need to change some things around feel free to contribute!

## Usage

Create a virtual environment using the requirements.txt Then to run the program you will need an input file. That can be given using the run arguments, the program will create an output bib file. The output file must also be specified in the execution command.

```
python3 bib-sort.py input/input_example.bib output/output.bib
```

## Adding keys

The citiation keys are specified using a separate json file. As an example I have provided the [input_example.bib](input/input_example.bib) file. To process these files I make use of the author keys in the [author_keys_example.json](configuration/author_keys_example.json). The keys can be added here as a dictionary like structure.