import csv
import re
import argparse

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
    # Thanks to Austin Crinklaw
    pattern = re.compile(r"[^A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]", re.IGNORECASE)
    has_amino_acids = pattern.findall(pep_seq)
    if has_amino_acids:
        return f"Peptide sequence {pep_seq} has characters {has_amino_acids} that are not amino acids"
    if mod_pos and not mod_type:
        return "Modificiation position provided but no modification type"
    if mod_type and not mod_pos:
        return "Modification type provided but not modification position"
    if mod_pos:
        modifications = mod_pos.replace(" ", "").split(",")
        if mod_type:
            mod_types = mod_type.replace(" ", "")
            mod_types = mod_types.split(",")
            num_mod_types = len(mod_types)
            num_mod_pos = len(modifications)
            if num_mod_pos != num_mod_types:
                return f"Error: There are {num_mod_pos} positions but {num_mod_types} modification types"
        statement = validate_mod_pos(pep_seq, modifications)
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


def validate_mod_pos(pep_seq, modifications):
    try:
        for mod in modifications:
            if len(mod) >= 2:
                position = "".join(mod[1:])
                position = int(position) - 1
                if pep_seq[position] is not mod[0]:
                    return f"This peptide sequence {pep_seq} does not contain {mod[0]} at position {mod[1]}"
            else:
                return f"There are {len(mod)} characters in one of the modification positions"
    except ValueError as v:
        return (
            f"ValueError.  {position} should be an integer.\n Here is the error message from the system: "
            + str(v)
        )
    except TypeError as t:
        return (
            f"TypeError. Perhaps there is bad value.\n Here is the error message from the system: "
            + str(t)
        )
    except IndexError as i:
        return (
            f"IndexError.  {position + 1} is greater than number of amino acids in peptide sequence {pep_seq}\n Here is the error message from the system: "
            + str(i)
        )
    return None


def test_validate_one():
    assert (
        validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="K5")
        == "This peptide sequence NLVPMVATV does not contain K at position 5"
    )


def test_validate_two():
    assert validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="M5") == None


def test_mod_pos_val_one():
    assert validate_mod_pos(pep_seq="NLVPMVATV", modifications=[("M", 5)]) == None


def test_mod_pos_val_two():
    assert (
        validate_mod_pos(pep_seq="NLVPMVATV", modifications=[("K", 5)])
        == "This peptide sequence NLVPMVATV does not contain K at position 5"
    )


def test_mod_pos_val_three():
    assert (
        validate_mod_pos(pep_seq="NLVPOVATV", modifications=[("M", 5)])
        == "This peptide sequence NLVPOVATV does not contain M at position 5"
    )
