"""Transforms bib files to include everything.

Bibtexparser imports the entries with problems as comments. In this script the comments
are processed. The problem is that the entries do not get a citationKey, therefore we 
have a json file to specify the citation key for certain authors. This script looks if the 
author in a comment has a citation key specified in the json file. In that case it adds the
citation key and adds the entry to the bibliography.

Finally it is exported to a bib file to use in latex.
"""
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bibdatabase import STANDARD_TYPES
import argparse
import json


def add_citation_key(entry: str, new_key: str) -> str:
    """Add citationkey after the { ."""
    ix = entry.find("{")
    return entry[: ix + 1] + new_key + entry[ix + 1 :]


def check_type(entry: str) -> bool:
    """Check if the entry type is one of the standard types.

    Args:
        entry: The entry we need to check.

    Returns:
        True in case of an existing standard type. and False if it does not exist.
    """
    attx = entry.find("@")
    ix = entry.find("{")
    type_bib = entry[attx + 1 : ix]
    return type_bib in STANDARD_TYPES


def retrieve_author(comment_entry: str) -> str:
    """Retrieve the author from an entry as a comment.

    Args:
        - comment_entry (str): the comment to search through.

    Returns:
        - author (str): the author string from the comment.
    """
    author_word_index = comment_entry.index("author")
    start_bracket = comment_entry[author_word_index:].index("{")
    close_bracket = comment_entry[author_word_index:].index("}")
    author = comment_entry[
        author_word_index + start_bracket + 1 : author_word_index + close_bracket
    ]
    return author


def retrieve_author_keys(json_filename: str) -> dict:
    """Retrieve the author keys from a json file.

    Args:
        json_filename: the filename where we get the author keys from.

    Returns:
        dict of author keys. {"author_name": "author_key"}
    """
    input_file = open(json_filename)
    data = json.load(input_file)
    input_file.close()
    if "author_id_keys" in data and isinstance(data["author_id_keys"], dict):
        return data["author_id_keys"]
    else:
        return {}


def process_author_keys_json(
    bib_database: BibDatabase, parser: BibTexParser, json_filename: str
) -> BibDatabase:
    """Process the comments using the author keys from a json file.

    Args:
        bib_database: the database we are building.
        parser: the bibtexparser to parse the entries.
        json_filename: name of the json file with the author names and keys.

    Returns
        bib_database: with the comments correctly processed.
    """
    author_keys = retrieve_author_keys(json_filename)

    removeComments = []
    # Addin the keys - future to do is add using a json file - very meta driven.
    for comment in bib_database.comments:
        parse = False
        print(comment)
        author = retrieve_author(comment)
        if author in author_keys:
            author_key = author_keys[author]
            newEntry = add_citation_key(comment, author_key)
            parse = True
        else:
            print(f"Author ({author}) not found in json.")

        if parse:
            if check_type(newEntry):
                try:
                    bib_database = bibtexparser.loads(newEntry, parser)
                    removeComments.append(comment)
                except:
                    print("There was a problem with the loading of the entry.")
                    pass
            else:
                print("Failed because of a wrong type for {}".format(newEntry))
    for rmComment in removeComments:
        bib_database.comments.remove(rmComment)
    return bib_database


def main():
    """Combine the different methods to transform the bib file."""
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("path", type=str)
    args_parser.add_argument("output_path", type=str)
    args = args_parser.parse_args()

    parser = BibTexParser()
    parser.customization = homogenize_latex_encoding
    with open(args.path, "r") as bib_file:
        bib_database = bibtexparser.load(bib_file, parser=parser)

    process_author_keys_json(
        bib_database, parser, "configuration/msc-thesis-author_keys.json"
    )

    writer = BibTexWriter()
    writer.indent = "\t"
    with open(args.output_path, "w") as bibfile:
        bibfile.write(writer.write(bib_database))


if __name__ == "__main__":
    main()
