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


    messages = []
    for row in rows:
        message = validate(
            pep_seq=row[0].value, mhc_name=row[3].value,
            mod_type=row[1].value, mod_pos=row[2].value
        )
        if message:
            messages.append(message)
        else:
            messages.append(f"Peptide sequence {row[0].value} is valid")
    generate_messages_txt(messages)
    return "Please see messages.txt for any errors"

def parse_csv_tsv(filename, delimiter):
    with open(filename, "r", encoding='utf-8-sig') as file_obj:
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        messages = []
        for entry in reader:
            messaage = validate(pep_seq = entry["Peptide Sequence"],
                   mhc_name=entry["MHC Name"],mod_type = entry["Modification Type"],
                   mod_pos=entry["Modification Position"])
            messages.append(message)
        generate_messages_txt(messages)
        return "Please see messages.txt for any errors"
        
def generate_messages_txt(messages, filename="messages.txt"):
    cwd = getcwd()
    new_file = path.join(cwd, filename)
    message_file = open(new_file, "w+")
    for message in messages:
        message_file.write(message)
        message_file.write("\n")
    message_file.close()
