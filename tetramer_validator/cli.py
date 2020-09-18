import argparse
from tetramer_validator.parse_tables import parse_csv_tsv, parse_excel_file
from os import getcwd, path

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser()
    file_help_text = """Please enter .tsv, .csv, or .xlsx filename.
        \n \n Please make sure header and columns are in the following order:
        Peptide Sequence, Modification Type, Modification Position, MHC name"""
    out_help_text = "Enter output file text name.  Default is messages.txt"
    parser.add_argument("-f", "--filename", required=True, help=file_help_text)
    parser.add_argument("-o", "--output", required=False, help = out_help_text)

    args = parser.parse_args()
    filename = args.filename
    output_file = args.output
    if filename.endswith(".tsv"):
        print("Parsing TSV file")
        messages = parse_csv_tsv(filename, delimiter="\t")
    elif filename.endswith(".csv"):
        print("Parsing CSV file")
        messages = parse_csv_tsv(filename, delimiter=",")
    elif filename.endswith(".xlsx"):
        print("Parsing Excel file")
        messages = parse_excel_file(filename)
    else:
        print("""Sorry, file is not valid format.
           Must be .tsv, .csv, or .xlsx file""")
        quit()
    if messages:
        if output_file:
            generate_messages_txt(messages, output_file)
        else:
            generate_messages_txt(messages)

if __name__ == "__main__":
    main()

def generate_messages_txt(messages, filename="messages.txt"):
    cwd = getcwd()
    new_file = path.join(cwd, filename)
    message_file = open(new_file, "w+")
    for message in messages:
        message_file.write(message)
        message_file.write("\n")
    message_file.close()
    print(f"Please see {filename} for any errors")
