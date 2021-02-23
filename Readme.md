## Readme for BibtexOrganiser

Using the bibtexparser.

The Mendeley online export function had problems with the generation of some citationkeys. I used the bibtexparser package to write a small python program to format my bibliography easier for my Master's thesis. It turned out that the package also had an option to format some encoding text, which I corrected manually in the past. A win-win so to say.


## Usage

create a virtual environment using python and source it. 
```
python3 -m venv testVenv
source testVenv/bin/activate
pip install -r requirements.txt
```

One can run the program as follows where input.bib is the input bibliography and output.bib is the output bibliography.
```
python3 bib-sort.py input.bib output.bib
```

## Adding keys

The problem I had was that for some reason Mendeley did not export keys. So I had to manually add them, as this was a straightforward process it could be easily programmed. In the if statement in the middle of the code is some logic defined to change comments into correct bib entries. One can change it or define it for itself. 

The aim in the future is to make this meta driven, so there will be a separate file containing the search criteria and key results.
