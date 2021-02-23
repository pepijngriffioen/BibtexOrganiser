import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bibdatabase import STANDARD_TYPES
import argparse


def addCitationKey(entry, newKey):
    ix = entry.find('{')
    return entry[:ix+1] + newKey + entry[ix+1:]

def checkType(entry):
    attx = entry.find('@')
    ix = entry.find('{')
    typeBib = entry[attx+1:ix]
    return typeBib in STANDARD_TYPES

def main():
    argsParser = argparse.ArgumentParser()
    argsParser.add_argument('path', type=str)
    argsParser.add_argument('output_path', type=str)
    args = argsParser.parse_args()

    parser = BibTexParser()
    parser.customization = homogenize_latex_encoding

    with open(args.path, 'r') as bib_file:
        bib_database = bibtexparser.load(bib_file, parser=parser)

    removeComments = []
    #Addin the keys - future to do is add using a json file - very meta driven.
    for comment in bib_database.comments:
        parse = False
        print(comment)
        if "{Object Management Group}" in comment:
            newEntry = addCitationKey(comment, "OmgUML")
            parse = True
        elif "{Javier J. Gutiérrez and Clémentine Nebut and María J. Escalona and Manuel Mejías and Isabel M. Ramos}" in comment:
            newEntry = addCitationKey(comment, "Gutierrez2008")
            parse = True
        
        if parse:
            if checkType(newEntry):
                try:
                    bib_database = bibtexparser.loads(newEntry, parser)
                    removeComments.append(comment)
                except:
                    pass
            else:
                print("Failed because of a wrong type for {}".format(newEntry))

    for rmComment in removeComments:
        bib_database.comments.remove(rmComment)

    writer = BibTexWriter()
    writer.indent = '\t'
    with open(args.output_path,'w') as bibfile:
        bibfile.write(writer.write(bib_database))

if __name__ == '__main__':
    main()