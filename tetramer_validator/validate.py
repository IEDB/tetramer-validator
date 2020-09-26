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

errors = []
with open(PTM_file) as fh_1:
    reader = csv.DictReader(fh_1, delimiter="\t")
    PTM_display = [name["display_name"] for name in reader]


def generate_problem_table(level, rule_name, value, instructions, fix=None):
    errors.append(locals())


def validate(pep_seq, mhc_name, mod_type=None, mod_pos=None):
    """Main validate function."""
    args = locals()
    properNumArguments(args)
    null_input_check(args)
    if errors:
        return errors
    if mod_pos and mod_type:
        validate_peptide(pep_seq, mod_type, mod_pos)

    validate_mhc_name(mhc_name)

    return errors


def properNumArguments(args):
    """Checks for proper number and combination of arguments for validate function"""

    incorrect_num_str = "IncorrectNumArgs"

    if not args["pep_seq"]:
        generate_problem_table(
            level="error",
            rule_name=incorrect_num_str,
            value=args["pep_seq"],
            instructions="Enter peptide sequence",
        )

    if not args["mhc_name"]:
        generate_problem_table(
            level="error",
            rule_name=incorrect_num_str,
            value=args["mhc_name"],
            instructions="Enter MHC molecule",
        )

    if args["mod_pos"] and not args["mod_type"]:
        generate_problem_table(
            level="error",
            rule_name=incorrect_num_str,
            value=args["mod_type"],
            instructions="Provide modificiation type(s)",
        )

    if args["mod_type"] and not args["mod_pos"]:
        generate_problem_table(
            level="error",
            rule_name=incorrect_num_str,
            value=args["mod_pos"],
            instructions="Provide modificiation position(s)",
        )

def null_input_check(args):
    null_rule_name = "NullValueEntered"
    null_strs = [
        "#N/A",
        "#N/A",
        "N/A",
        "#NA",
        "-1.#IND",
        "-1.#QNAN",
        "-NaN",
        "-nan",
        "1.#IND",
        "1.#QNAN",
        "NA",
        "NULL",
        "NaN",
        r"n/a",
        "nan",
        "null",
        "<NA>",
        "N/A",
    ]
    for (param, value) in args.items():
        if value in null_strs:
            if param == "pep_seq":
                generate_problem_table(
                    level="error",
                    rule_name=null_rule_name,
                    value=value,
                    instructions="Please do not enter any null string."
                    " Peptide sequence is required",
                )
            elif param == "mhc_name":
                generate_problem_table(
                    level="error",
                    rule_name=null_rule_name,
                    value=value,
                    instructions="Please do not enter any null string."
                    " MHC molecule is required",
                )
            else:
                generate_problem_table(
                    level="error",
                    rule_name=null_rule_name,
                    value=value,
                    fix="",
                    instructions="Please do not enter any null string."
                    " Leave blank if needed",
                )


def validate_amino_acids(pep_seq):
    """Thanks to Austin Crinklaw.  Simple function to validate if given string has valid amino
    acids letters"""

    aa_rule_name = "UnrecognizedAminoAcid"
    pattern = re.compile(r"[^A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]", re.IGNORECASE)
    has_amino_acids = pattern.findall(pep_seq)
    if has_amino_acids:
        generate_problem_table(
            level="error",
            rule_name=aa_rule_name,
            value=pep_seq,
            instructions=f"The peptide sequence has characters {has_amino_acids}"
            " that are not amino acids",
        )


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

    invalid_PTM_rule = "InvalidPTMtype"
    for type in mod_types:
        if type not in PTM_display:
            generate_problem_table(
                level="error",
                rule_name=invalid_PTM_rule,
                value=type,
                instructions="Please choose a post-translational type from the autocomplete list",
            )


def validate_mod_pos_syntax(pep_seq, positions):
    """Given list of modification positions, validates list against syntax of amino acid followed
    by position number (e.g. ['N1', 'N100'])"""

    main_pattern = re.compile(
        r"[A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]\d+", re.IGNORECASE
    )
    digits = re.compile(r"\d+")
    reversed_pattern = re.compile(
        r"\d+[A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y]", re.IGNORECASE
    )
    just_digits = "JustDigits"
    reversed = "ReverseAminoAcid"
    general = "GeneralModPos"
    for pos in positions:
        if re.fullmatch(main_pattern, pos) is None:
            formatted_string = (
                f"{pos} is not a valid modification position."
                "Modification Position field should be a comma separated list of amino acid "
                "letter followed by position number (e.g. F1, S10, S300) "
            )

            if re.fullmatch(pattern=digits, string=pos):
                if int(pos) > len(pep_seq):
                    generate_problem_table(
                        level="error",
                        rule_name=just_digits,
                        value=pos,
                        instructions=formatted_string + "This input is just digit(s)",
                    )
                else:
                    generate_problem_table(
                        level="error",
                        rule_name=just_digits,
                        fix=str(pep_seq[int(pos) - 1] + pos),
                        value=pos,
                        instructions=formatted_string
                        + "Enter amino acid before digit(s)",
                    )

            elif re.fullmatch(pattern=reversed_pattern, string=pos):
                generate_problem_table(
                    level="error",
                    rule_name=reversed,
                    fix=f"{pos[-1]}{pos[:-1]}",
                    value=pos,
                    instructions=formatted_string
                    + "Enter amino acid followed by position.",
                )

            else:
                generate_problem_table(
                    level="error",
                    rule_name=general,
                    value=pos,
                    instructions=formatted_string,
                )


def validate_peptide(pep_seq, mod_pos, mod_type):
    """Main helper function to validate, checks for validation of peptide sequence, modification
    position, and modification type"""

    validate_amino_acids(pep_seq)

    positions, mod_types = format_mod_info(mod_pos)

    trailing_rule_name = "TrailingCharacters"
    trailing_characters = re.findall(
        r"[^A|C|D|E|F|G|H|I|K|L|M|N|P|Q|R|S|T|V|W|X|Y\d]+$", positions
    )
    if trailing_characters:
        generate_problem_table(
            level="error",
            rule_name=trailing_rule_name,
            value=mod_pos,
            instructions=f"Remove {trailing_characters} from modification position",
        )

    positions = positions.split(",")
    mod_types = mod_types.split(",")
    validate_PTM_names(mod_types)
    validate_mod_pos_syntax(pep_seq, positions)

    num_mod_types = len(mod_types)
    num_mod_pos = len(positions)
    mod_num_mismatch = "NumModPosTypeMismatch"
    if num_mod_pos < num_mod_types:
        generate_problem_table(
            level="warn",
            rule_name=mod_num_mismatch,
            value=mod_pos,
            instructions="Decrease number of modification types"
            " or increase number of modification positions",
        )
    if num_mod_types < num_mod_pos:
        generate_problem_table(
            level="warn",
            rule_name=mod_num_mismatch,
            value=mod_type,
            instructions="Decrease number of modification positions"
            " or increase number of modification types",
        )

    validate_mod_pos(pep_seq, positions)
    return errors


def validate_mhc_name(mhc_name):
    """Check if given MHC name match up to MRO name"""
    invalid_MHC_rule = "InvalidMHCmol"
    if mhc_name not in molecules:
        generate_problem_table(
            level="error",
            rule_name=invalid_MHC_rule,
            value=mhc_name,
            instructions="Enter MHC molecule from prepopulated list",
        )


def validate_mod_pos(pep_seq, positions):
    """Validates the list of modification positions (in proper syntax) for peptide sequence entered
    as occuring at the stated position."""

    pos_pep_seq_rule = "AminoAcidPosMismatch"
    try:
        for pos in positions:
            if len(pos) >= 2:
                position = "".join(pos[1:])
                position = int(position) - 1
                if pep_seq[position] is not pos[0]:
                    part_one = "This peptide sequence "
                    part_two = f"does not contain {pos[0]} at position {pos[1:]}. "
                    result = part_one + part_two
                    generate_problem_table(
                        level="error",
                        rule_name=pos_pep_seq_rule,
                        value=pos,
                        instructions=result
                        + "Enter a amino acid letter and matching position from peptide sequence",
                    )

    except IndexError:
        index_rule = "PosGreaterPepLen"
        formatted_string = (
            f"IndexError. {position + 1} is greater than number of"
            " amino acids in peptide sequence. "
        )
        generate_problem_table(
            level="error",
            rule_name=index_rule,
            value=int(pos[1:]),
            instructions=formatted_string
            + "Enter position that is less than length of peptide sequence and more than 0.",
        )
