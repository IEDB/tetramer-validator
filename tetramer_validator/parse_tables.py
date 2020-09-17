

def parse_excel_file(filename):
    wb = load_workbook(filename)
    ws = wb.active
    column_count = ws.max_column
    if column_count != 4:
        return "Need to have 4 columns in following order: Peptide Sequence, Modification Type, Modification Position, MHC Name"
    header = [entry.value for entry in ws[1]]
    print(header)
    rows = ws.iter_rows(min_row=2)
    messages = open("messages.txt")
    for row in rows:
        message = validate(
            pep_seq=row[1], mhc_name=row[4], mod_type=row[2], mod_pos=row[3]
        )


def parse_csv_tsv(filename, delimiter):
    with open(filename, "r") as file_obj:
        reader = csv.DictReader(file_obj, delimiter=delimiter)
