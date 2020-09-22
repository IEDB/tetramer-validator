from tetramer_validator.validate import validate
from openpyxl import load_workbook
import csv


def parse_excel_file(filename):
    wb = load_workbook(filename)
    ws = wb.active
    messages = []
    header = {
        "Peptide Sequence": -1,
        "Modification Type": -1,
        "Modification Position": -1,
        "MHC Name": -1,
    }
    for entry in ws[1]:
        if entry in header.keys():
            header[entry] = entry.column - 1

    if -1 in header.values():
        messages.append(
            "Need to have 4 columns in first row: Peptide Sequence, "
            "Modification Type, Modification Position, and MHC Name"
        )
        return messages
    rows = ws.iter_rows(min_row=2)

    for row in rows:
        message = validate(
            pep_seq=row[header["Peptide Sequence"]].value,
            mhc_name=row[header["Modification Type"]].value,
            mod_type=row[header["Modification Position"]].value,
            mod_pos=row[header["MHC Name"]].value,
        )
        if message:
            messages.append(message)
        else:
            messages.append(f"Peptide sequence {row[0].value} is valid")
    return messages


def parse_csv_tsv(filename, delimiter):
    with open(filename, "r", encoding="utf-8-sig") as file_obj:
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        messages = []
        for entry in reader:
            message = validate(
                pep_seq=entry["Peptide Sequence"],
                mhc_name=entry["MHC Name"],
                mod_type=entry["Modification Type"],
                mod_pos=entry["Modification Position"],
            )
            if message:
                messages.append(message)
            else:
                pep_seq = entry["Peptide Sequence"]
                messages.append(f"Peptide sequence {pep_seq} is valid")
        return messages
