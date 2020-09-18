from tetramer_validator.validate import validate
from openpyxl import load_workbook
import csv
from os import getcwd, path

def parse_excel_file(filename):
    wb = load_workbook(filename)
    ws = wb.active
    column_count = ws.max_column

    #if column_count != 4:
        #return """Need to have 4 columns in following order: Peptide Sequence,
        # Modification Type, Modification Position, MHC Name"""
    header = [entry.value for entry in ws[1]]

    rows = ws.iter_rows(min_row=2)
    cwd = getcwd()
    new_file = path.join(cwd, "messages.txt")

    messages = open(new_file, "w+")
    for row in rows:
        message = validate(
            pep_seq=row[0].value, mhc_name=row[3].value, mod_type=row[1].value, mod_pos=row[2].value
        )
        if message:
            messages.write(message)
        else:
            messages.write(f"Peptide sequence {row[0].value} is valid")
        messages.write("\n")
    messages.close()
    return "Please see messages.txt for any errors"

def parse_csv_tsv(filename, delimiter):
    with open(filename, "r") as file_obj:
        reader = csv.DictReader(file_obj, delimiter=delimiter)
