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


def validate(pep_seq, mhc_name, mod_type=None, mod_pos=None):
    """Main validate function."""
    args = locals()
    statement = properNumArguments(args)
    if statement:
        return statement
    if mod_pos and mod_type:
        validate_peptide(pep_seq, mod_type, mod_pos)

    statement = validate_pep_seq_mhc_name(pep_seq, mhc_name)
    if statement:
        return statement
    return None


def properNumArguments(args):
    """Checks for proper number and combination of arguments for validate function"""

    incorrect_num_str = "Incorrect number of arguments:"

    if not args["pep_seq"]:
        return "".join(incorrect_num_str, "Peptide sequence is required")
    if not args["mhc_name"]:
        return "".join(incorrect_num_str, "MHC molecule required")
    if args["mod_pos"] and not args["mod_type"]:
        return (
            "Incorrect number of arguments: Modificiation position provided"
            " but no modification type"
        )
    if args["mod_type"] and not args["mod_pos"]:
        return (
            "Incorrect number of arguments: Modification type provided"
            " but not modification position"
        )

    null_str = "NULL"
    if null_str in args.values():
        return "NULL value entered. If there is no need for a particular value, please leave blank."

    return None


def validate_amino_acids(pep_seq):
    """Thanks to Austin Crinklaw.  Simple function to validate if given string has valid amino
    acids letters"""
    pattern = re.compile(r"[^A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]", re.IGNORECASE)
    has_amino_acids = pattern.findall(pep_seq)
    if has_amino_acids:
        return (
            f"Unrecognized amino acid: Peptide sequence {pep_seq} has characters {has_amino_acids} "
            "that are not amino acids"
        )
    return None


def format_mod_info(mod_pos, mod_type):
    """Simple helper function to turn strings that have modification position and modification
    types into lists and remove whitespace"""

    mod_pos = str(mod_pos)
    pattern = re.compile(r",[\s]+")
    positions = re.sub(pattern, ",", mod_pos)
    mod_types = mod_type
    mod_types = re.sub(pattern, ",", mod_types)
    return positions, mod_types


def validate_PTM_names(mod_types):
    """Check if given list of modification types match up to MOD list"""
    for type in mod_types:
        if type not in PTM_display:
            return f"{type} is not a valid modification type"


def validate_mod_pos_syntax(positions):
    """Given list of modification positions, validates list against syntax of amino acid followed
    by position number (e.g. ['N1', 'N100'])"""

    main_pattern = re.compile(
        r"[A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]\d+", re.IGNORECASE
    )
    digits = re.compile(r"\d+")
    reversed_pattern = re.compile(
        r"\d+[A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]", re.IGNORECASE
    )
    for pos in positions:
        if re.fullmatch(main_pattern, pos) is None:
            formatted_string = (
                f"{pos} is not a valid modification position."
                "Modification Position field should be a comma separated list of amino acid "
                "letter followed by position number (e.g. F1, S10, S300)"
            )
            if re.fullmatch(pattern=digits, string=pos):
                return formatted_string + "This input is just digit(s)"
            elif re.fullmatch(pattern=reversed_pattern, string=pos):
                return (
                    formatted_string
                    + "This input has syntax reversed syntax."
                    + f"Should be {pos[-1]}{pos[:-1]}"
                )
            else:
                return formatted_string
    return None


def validate_peptide(pep_seq, mod_pos, mod_type):
    """Main helper function to validate.py, checks for validation of peptide sequence, modification
    position, and modification type"""
    statement = validate_amino_acids(pep_seq)

    if statement:
        return statement

    positions, mod_types = format_mod_info(mod_pos)

    trailing_characters = re.findall(
        r"[^A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y\d]+$", positions
    )
    if trailing_characters:
        return (
            f"FormatError: {trailing_characters} at the end of input {mod_pos}"
            " are unrecognized"
        )

    positions = positions.split(",")
    mod_types = mod_types.split(",")

    statement = validate_mod_pos_syntax(positions)
    if statement:
        return statement

    num_mod_types = len(mod_types)
    num_mod_pos = len(positions)
    if num_mod_pos != num_mod_types:
        return (
            f"MismatchError: There are {num_mod_pos} positions but {num_mod_types}"
            " modification types"
        )

    statement = validate_PTM_names(mod_types)
    if statement:
        return statement

    statement = validate_mod_pos(pep_seq, positions)
    if statement:
        return statement

    return None


def validate_pep_seq_mhc_name(pep_seq, mhc_name):
    """Check if given MHC name match up to MRO name"""
    if mhc_name not in molecules:
        return f"{mhc_name} is not a valid MHC molecule name"
    return None


def validate_mod_pos(pep_seq, positions):
    """Validates the list of modification positions (in proper syntax) for peptide sequence entered
    as occuring at the stated position."""
    try:
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

    except IndexError as i:
        formatted_string_one = (
            f"IndexError. {position + 1} is greater than number of amino acids in "
        )
        formatted_string_two = f"peptide sequence {pep_seq}."
        system_err_pre = "Here is the error message from the system: "
        final_string = (
            formatted_string_one + formatted_string_two + "\n" + system_err_pre + str(i)
        )
        return final_string
    return None
