import argparse
from tetramer_validator.parse_tables import parse_csv_tsv, parse_excel_file


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser()
    filename_help_text = """Please enter .tsv, .csv, or .xlsx filename.
        \n \n Please make sure header and columns are in the following order:
        Peptide Sequence, Modification Type, Modification Position, MHC name"""
    parser.add_argument("-f", "--filename", required=True, help=filename_help_text)
    args = parser.parse_args()
    with open(args.filename, "r") as file_obj:
        if filename.endwith(".tsv"):
            parse_csv_tsv(filename, delimiter="\t")
        elif filename.endswith(".csv"):
            parse_csv_tsv(filename, delimiter=",")
        elif filename.endswith(".xlsx"):
            parse_excel_file(filename)
        else:
            print(
                """Sorry, file is not valid format.
                Must be .tsv, .csv, or .xlsx file"""
            )
            quit()


print(__name__)
if __name__ == "__main__":
    main()
