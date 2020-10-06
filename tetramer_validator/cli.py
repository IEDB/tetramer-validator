import argparse
from tetramer_validator.parse_tables import parse_csv_tsv, parse_excel_file, generate_messages_txt
from os import getcwd, path
import sys
import shutil

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser()
    file_help_text = """Please enter .tsv, .csv, or .xlsx filename
        and that header is in following order:
        Peptide Sequence, Modification Type, Modification Position, MHC Molecule"""
    out_help_text = "Enter output file text name."
    parser.add_argument("filename", help=file_help_text)
    parser.add_argument("-o", "--output", required=False, help=out_help_text)

    args = parser.parse_args()
    filename = args.filename
    output_file = args.output
    messages = []
    any_error = False
    if filename.endswith(".tsv"):
        messages, any_error = parse_csv_tsv(filename, delimiter="\t")
    elif filename.endswith(".csv"):
        messages, any_error = parse_csv_tsv(filename, delimiter=",")
    elif filename.endswith(".xlsx"):
        messages, any_error = parse_excel_file(filename)
    else:
        print("Sorry, file is not valid format. Must be .tsv, .csv, or .xlsx file")
        sys.exit(1)
    if any_error:
        if output_file:
            file_obj = open(output_file, "w")
            generate_messages_txt(messages, file_obj)
        else:
            for message in messages:
                print(message)
    return sys.exit(any_error)


if __name__ == "__main__":
    main()
