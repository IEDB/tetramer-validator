import argparse
import validate


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser()
    filename_help_text = "Please enter .tsv, .csv, or .xlsx filename.  \nPlease make sure header and columns are in the following order: Peptide Sequence, Modification Type, Modification Position, MHC name"
    parse.add_argument("-f", "--filename", required=True, help=filename_help_text)
    args = parser.parse_args()
    if args.filename.endwith(".tsv"):
        parse_csv_tsv(filename, delimiter="\t")
    elif args.filename.endswith(".csv"):
        parse_csv_tsv(filename, delimiter=",")
    elif args.filename.endswith(".xlsx"):
        parse_excel_file(filename)
    else:
        print("Sorry, file is not valid format.  Must be .tsv, .csv, or .xlsx file")
        quit()


if __name__ == "__main__":
    main()
