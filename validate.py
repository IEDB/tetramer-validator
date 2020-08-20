import csv

path = "molecule.tsv"
with open(path) as fh:
    reader = csv.DictReader(fh, delimiter="\t")
    molecules = [
        molecule["IEDB Label"]
        for molecule in reader
        if molecule["Restriction Level"] == "complete molecule"
        or molecule["Restriction Level"] == "partial molecule"
    ]


def validate(pep_seq, mhc_name, mod_type=None, mod_pos=None):
    if mod_pos:
        statement = validate_mod_pos(pep_seq, mod_pos)
        if statement:
            return statement
    if mhc_name:
        statement = validate_pep_seq_mhc_name(pep_seq, mhc_name)
        if statement:
            return statement

    return None


def validate_pep_seq_mhc_name(pep_seq, mhc_name):
    if mhc_name not in molecules:
        return f"{mhc_name} is not a valid MHC name"
    return None
    # Need to know how to match mhc_name with pep_seq
    # elif mhc_name:
    # else:
    # return None


def validate_mod_pos(pep_seq, mod_pos):
    split = mod_pos.split(",")
    modifications = [(mod[0], int(mod[1])) for mod in split]
    pep_seq_tuple = [(peptide, index) for index, peptide in enumerate(pep_seq)]

    for mod in modifications:
        if mod not in pep_seq_tuple:
            return f"This peptide sequence {pep_seq} does not contain {mod[0]} at position {mod[1]}"
    return None


def test_validate_one():
    assert (
        validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="K4")
        == "This peptide sequence NLVPMVATV does not contain K at position 4"
    )


def test_validate_two():
    assert validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="M4") == None


def test_mod_pos_val_one():
    assert validate_mod_pos(pep_seq="NLVPMVATV", mod_pos="M4") == None


def test_mod_pos_val_two():
    assert (
        validate_mod_pos(pep_seq="NLVPMVATV", mod_pos="K4")
        == "This peptide sequence NLVPMVATV does not contain K at position 4"
    )


def test_mod_pos_val_three():
    assert (
        validate_mod_pos(pep_seq="NLVPOVATV", mod_pos="M4")
        == "This peptide sequence NLVPOVATV does not contain M at position 4"
    )
