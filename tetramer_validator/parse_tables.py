from tetramer_validator.validate import validate
from openpyxl import load_workbook
import csv
from openpyxl.styles import Color, PatternFill
from openpyxl.comments import Comment

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
        if entry.value in header.keys():
            header[entry.value] = entry.column - 1

    if -1 in header.values():
        messages.append(
            "Need to have 4 columns in first row: Peptide Sequence, "
            "Modification Type, Modification Position, and MHC Name"
        )
        return messages
    rows = ws.iter_rows(min_row=2)
    any_errors = False
    for row in rows:
        message = validate(
            pep_seq=row[header["Peptide Sequence"]].value,
            mod_type=row[header["Modification Type"]].value,
            mod_pos=row[header["Modification Position"]].value,
            mhc_name=row[header["MHC Name"]].value,
        )
        if message:
            messages.append(message)
            any_errors = True
        else:
            messages.append(f"Peptide sequence {row[0].value} is valid")
    return (messages, any_errors)


def parse_csv_tsv(filename, delimiter):
    any_errors = False
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
                any_errors = True
            else:
                pep_seq = entry["Peptide Sequence"]
                messages.append(f"Peptide sequence {pep_seq} is valid")
    return (messages, any_errors)

def generate_formatted_data(data_path, problems):
    wb = load_workbook(data_path)
    ws = wb.active
    for problem in problems:
        cell = ws[problem["cell"]]
        if problem["level"] == "error":
            cell.fill = PatternFill(
                patternType="lightUp", fgColor=Color(indexed=10), fill_type="solid"
            )
        else:
            cell.fill = PatternFill(
                patternType="lightUp", fgColor=Color(indexed=52), fill_type="solid"
            )
        if cell.comment:
            comment = Comment(
                cell.comment.text + "\n" + problem["message"],
                author="tetramer_validator",
            )
            cell.comment = comment
        else:
            cell.comment = Comment(problem["message"], author="tetramer-validator")
    wb.save(data_path)
