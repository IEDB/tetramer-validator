import csv
import re
from os import path

here = path.abspath(path.dirname(__file__))
molecule_file = "data/molecule.tsv"
molecule_file = path.join(here, molecule_file)
with open(molecule_file) as fh:
    reader = csv.DictReader(fh, delimiter="\t")
    molecules = [molecule["IEDB Label"] for molecule in reader]
PTM_file = "data/PTM_list.tsv"
PTM_file = path.join(here, PTM_file)

with open(PTM_file) as fh_1:
    reader = csv.DictReader(fh_1, delimiter="\t")
    PTM_display = [name["display_name"] for name in reader]


def validate(pep_seq, mhc_name=None, mod_type=None, mod_pos=None):
    args = locals()
    null_str = "NULL"
    if null_str in args.values():
        return "NULL value entered. If there is no need for a particular value, please leave blank."
    if "" == args["pep_seq"]:
        return "Incorrect number of arguments: Peptide sequence is required"
    if pep_seq != "" and mhc_name is None and mod_type is None and mod_pos is None:
        return (
            "Incorrect number of arguments: Please enter modification information "
            "and/or MHC molecule information."
        )
    # Thanks to Austin Crinklaw
    pattern = re.compile(r"[^A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]", re.IGNORECASE)
    has_amino_acids = pattern.findall(pep_seq)
    if has_amino_acids:
        return (
            f"Unrecognized amino acid: Peptide sequence {pep_seq} has characters {has_amino_acids} "
            "that are not amino acids"
        )
    if mod_pos and not mod_type:
        return (
            "Incorrect combination of arguments: Modificiation position provided"
            " but no modification type"
        )
    if mod_type and not mod_pos:
        return (
            "Incorrect combination of arguments: Modification type provided"
            " but not modification position"
        )
    if mod_pos:
        mod_pos = str(mod_pos)
        pattern = re.compile(r",[\s]+")
        positions = re.sub(pattern, ",", mod_pos)
        trailing_characters = re.findall(
            r"[^A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y\d]+$", positions
        )
        if trailing_characters:
            return (
                f"FormatError: {trailing_characters} at the end of input {mod_pos}"
                " are unrecognized"
            )
        positions = positions.split(",")
        if mod_type:
            mod_types = mod_type
            pattern = re.compile(r",[\s]+")
            mod_types = re.sub(pattern, ",", mod_types)
            mod_types = mod_types.split(",")
            num_mod_types = len(mod_types)
            num_mod_pos = len(positions)
            if num_mod_pos != num_mod_types:
                return (
                    f"MismatchError: There are {num_mod_pos} positions but {num_mod_types}"
                    " modification types"
                )
            for type in mod_types:
                if type not in PTM_display:
                    return f"{type} is not a valid modification type"
        statement = validate_mod_pos(pep_seq, positions)
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
        system_err_pre = "Here is the error message from the system: "
        if any(len(pos) > 0 and pos[0] not in amino_acids for pos in positions):
            return (
                "Modification position is just numbers without amino acid "
                "letter or format of modification position is incorrect "
                "(amino acid and position switched)"
            )
        for pos in positions:
            if len(pos) >= 2:
                position = "".join(pos[1:])
                position = int(position) - 1
                if pep_seq[position] is not pos[0]:
                    part_one = f"MismatchError: This peptide sequence {pep_seq} "
                    part_two = f"does not contain {pos[0]} at position {pos[1:]}"
                    result = part_one + part_two
                    return result
            else:
                return f"""There are {len(pos)} characters in one of the modification positions"""

    except ValueError as v:
        formatted_string = f"ValueError.  {position} should be an integer.\n "
        final_string = formatted_string + system_err_pre + str(v)
        return final_string
    except TypeError as t:
        return "TypeError. Perhaps there is bad value.\n " + system_err_pre + str(t)
    except IndexError as i:
        formatted_string_one = (
            f"IndexError. {position + 1} is greater than number of amino acids in "
        )
        formatted_string_two = f"peptide sequence {pep_seq}."
        final_string = (
            formatted_string_one + formatted_string_two + "\n" + system_err_pre + str(i)
        )
        return final_string
    return None
