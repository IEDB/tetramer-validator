import csv
import re
import math


def validate(pep_seq, mhc_name=None, mod_type=None, mod_pos=None):
    print(pep_seq)
    num_types_pos_mismatch = False
    # Thanks to Austin Crinklaw
    pattern = re.compile(r"[^A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]", re.IGNORECASE)
    if pep_seq == float("nan"):
        return "Peptide sequence is bad value (NULL) or is empty"
    has_amino_acids = pattern.findall(pep_seq)
    if has_amino_acids:
        return f"Peptide sequence {pep_seq} has characters {has_amino_acids} that are not amino acids"
    if mod_pos and not mod_type:
        return "Modificiation position provided but no modification type"
    if mod_type and not mod_pos:
        return "Modification type provided but not modification position"
    if mod_pos:
        mod_pos = str(mod_pos)
        modifications = mod_pos.replace(" ", "").split(",")
        if mod_type:
            mod_types = mod_type.replace(" ", "")
            mod_types = mod_types.split(",")
            num_mod_types = len(mod_types)
            num_mod_pos = len(modifications)
            if num_mod_pos != num_mod_types:
                num_types_pos_mismatch = f"""MismatchError: There are
                {num_mod_pos} positions but {num_mod_types} modification types"""
        statement = validate_mod_pos(pep_seq, modifications)
        if statement:
            return statement
    if mhc_name:
        statement = validate_pep_seq_mhc_name(pep_seq, mhc_name)
        if statement:
            return statement
        if num_types_pos_mismatch:
            return num_types_pos_mismatch
    return None


def validate_pep_seq_mhc_name(pep_seq, mhc_name):
    # if mhc_name not in molecules:
    #   return f"{mhc_name} is not a valid MHC name"
    return None
    # Need to know how to match mhc_name with pep_seq
    # elif mhc_name:
    # else:
    # return None


def validate_mod_pos(pep_seq, positions):
    amino_acids = [
        "A",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "K",
        "L",
        "M",
        "N",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "V",
        "W",
        "X",
        "Y",
    ]
    try:
        if any(len(pos) > 0 and pos[0] not in amino_acids for pos in positions):
            return """Modification position is just numbers without amino acid
                letter or format of modification position is incorrect (amino acid and position switched)"""
        for pos in positions:
            if len(pos) >= 2:
                position = "".join(pos[1:])
                position = int(position) - 1
                if pep_seq[position] is not pos[0]:
                    return f"MismatchError: This peptide sequence {pep_seq} does not contain {pos[0]} at position {pos[1]}"
            else:
                return f"There are {len(pos)} characters in one of the modification positions"
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
        return f"""IndexError.  {position + 1} is greater than number of amino acids in peptide sequence {pep_seq}.
                \n Here is the error message from the system: """ + str(
            i
        )
    return None
