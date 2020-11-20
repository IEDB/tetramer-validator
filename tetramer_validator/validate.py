import csv
import re
from os import path

here = path.abspath(path.dirname(__file__))
molecule_file = "data/molecule.tsv"
molecule_file = path.join(here, molecule_file)
with open(molecule_file) as fh:
    reader = csv.DictReader(fh, delimiter="\t")
    molecules = [molecule["IEDB Label"] for molecule in reader]

PTM_synonyms = {}

PTM_file = "data/PTM_list.tsv"
PTM_file = path.join(here, PTM_file)
with open(PTM_file) as fh_1:
    reader = csv.DictReader(fh_1, delimiter="\t")
    # PTM_temp = [name for name in reader]
    PTM_synonyms = {
        synonym: name["display_name"]
        for name in reader
        for synonym in name.values()
        if synonym is not None
    }


def validate(mhc_name, pep_seq, mod_type=None, mod_pos=None):
    """Main validate function."""
    args = locals()
    pep_seq = pep_seq.strip()
    mhc_name = mhc_name.strip()
    errors = []
    errors.extend(properNumArguments(args))
    errors.extend(null_input_check(args))

    if errors:
        return errors

    if pep_seq:
        errors.extend(
            validate_peptide(pep_seq=pep_seq, mod_type=mod_type, mod_pos=mod_pos)
        )

    errors.extend(validate_mhc_name(mhc_name))
    return errors


def properNumArguments(args):
    """Checks for proper number and combination of arguments for validate function"""

    errors = []
    incorrect_num_str = "IncorrectNumArgs"

    if not args["pep_seq"]:
        errors.append(
            {
                "level": "error",
                "rule": incorrect_num_str + "PepSeq",
                "value": args["pep_seq"],
                "field": "pep_seq",
                "message": "Peptide sequence missing. Enter peptide sequence.",
                "suggestion": None,
            }
        )

    if not args["mhc_name"]:
        errors.append(
            {
                "level": "error",
                "rule": incorrect_num_str + "MHCMol",
                "value": args["mhc_name"],
                "field": "mhc_name",
                "message": "MHC molecule missing. Enter MHC molecule.",
                "suggestion": None,
            }
        )

    if args["mod_pos"] and not args["mod_type"]:
        errors.append(
            {
                "level": "error",
                "rule": incorrect_num_str + "ModType",
                "value": args["mod_type"],
                "field": "mod_type",
                "message": "Modification position is filled, but modification type is not."
                " Provide modificiation type(s).",
                "suggestion": None,
            }
        )

    if args["mod_type"] and not args["mod_pos"]:
        errors.append(
            {
                "level": "error",
                "rule": incorrect_num_str + "ModPos",
                "value": args["mod_pos"],
                "field": "mod_pos",
                "message": "Modification type is filled, but modification position is not."
                " Provide modificiation position(s).",
                "suggestion": None,
            }
        )
    return errors


def null_input_check(args):
    errors = []
    null_rule_name = "UndefinedArgNullValue"
    null_strs = [
        "#N/A",
        "#N/A N/A",
        "#NA",
        "-1.#IND",
        "-1.#QNAN",
        "-NaN",
        "-nan",
        "1.#IND",
        "1.#QNAN",
        "<NA>",
        "N/A",
        "NA",
        "NULL",
        "NaN",
        "n/a",
        "nan",
        "null",
    ]
    for (param, value) in args.items():
        if value in null_strs:
            if param == "pep_seq":
                errors.append(
                    {
                        "level": "error",
                        "rule": null_rule_name,
                        "value": value,
                        "field": "pep_seq",
                        "message": "Please do not enter any null string."
                        " Peptide sequence is required",
                        "suggestion": None,
                    }
                )
            elif param == "mhc_name":
                errors.append(
                    {
                        "level": "error",
                        "rule": null_rule_name,
                        "value": value,
                        "field": "mhc_name",
                        "message": "Please do not enter any null string."
                        " MHC molecule is required",
                        "suggestion": None,
                    }
                )
            else:
                errors.append(
                    {
                        "level": "error",
                        "rule": null_rule_name,
                        "value": value,
                        "field": param,
                        "message": "Please do not enter any null string."
                        " Leave blank if needed",
                        "suggestion": None,
                    }
                )
    return errors


def validate_amino_acids(pep_seq):
    """Thanks to Austin Crinklaw.  Simple function to validate if given string has valid amino
    acids letters"""

    errors = []
    aa_rule_name = "UndefinedArgAminoAcid"
    pattern = re.compile(r"[^ACDEFGHIKLMNPQRSTVWXY]", re.IGNORECASE)
    has_amino_acids = pattern.findall(pep_seq)
    if has_amino_acids:
        errors.append(
            {
                "level": "error",
                "rule": aa_rule_name,
                "value": pep_seq,
                "field": "pep_seq",
                "message": f"The peptide sequence has characters {has_amino_acids}"
                " that are not amino acids. Please remove them.",
                "suggestion": None,
            }
        )
    return errors


def format_mod_info(mod_pos, mod_type):
    """Simple helper function to remove whitespace strings that have modification
    position and modification types"""

    mod_pos = str(mod_pos)
    pattern = re.compile(r",[\s]+")
    positions = re.sub(pattern, ",", mod_pos)
    mod_types = mod_type
    mod_types = re.sub(pattern, ",", mod_types)
    mod_types = mod_types.strip()
    positions = positions.strip()
    return positions, mod_types


def validate_PTM_names(mod_types):
    """Check if given list of modification types match up to MOD list"""
    errors = []
    invalid_PTM_rule = "UndefinedArgPTMtype"
    for type in mod_types:
        in_synonyms = type in PTM_synonyms.keys()
        if in_synonyms and not PTM_synonyms[type] == type:
            errors.append(
                {
                    "level": "error",
                    "rule": "ModTypeSynonymError",
                    "value": type,
                    "field": "mod_type",
                    "message": f"{type} is a synonym for {PTM_synonyms[type]}."
                    f" Please use {PTM_synonyms[type]}"
                    " to conform to PSI-MOD terminology.",
                    "suggestion": PTM_synonyms[type],
                }
            )
        elif not in_synonyms:
            errors.append(
                {
                    "level": "error",
                    "rule": invalid_PTM_rule,
                    "value": type,
                    "field": "mod_type",
                    "message": "Invalid entry for post-translational modification type."
                    " Please use post-translational modification type as cataloged in PSI-MOD.",
                    "suggestion": None,
                }
            )
    return errors


def validate_mod_pos_syntax(pep_seq, positions):
    """Given list of modification positions, validates list against syntax of amino acid followed
    by position number (e.g. ['N1', 'N100'])"""

    errors = []
    trailing_rule_name = "SyntaxErrorTrailingCharacters"
    main_pattern = re.compile(
        r"[ACDEFGHIKLMNPQRSTVWXY][\d+]", re.IGNORECASE
    )
    last_position = [y.span() for y in re.finditer(main_pattern, positions)]
    if last_position:
        last_position = last_position[-1:][0][1]
        trailing_characters = positions[last_position:]
        if trailing_characters:
            errors.append(
                {
                    "level": "error",
                    "rule": trailing_rule_name,
                    "value": positions,
                    "field": "mod_pos",
                    "message": "Syntax error in Modification Position field."
                    + f" Remove '{trailing_characters}' from Modification Position.",
                    "suggestion": None,
                }
            )
            return errors

    positions = positions.split(",")
    digits = re.compile(r"\d+")
    reversed_pattern = re.compile(
        r"[\d+][ACDEFGHIKLMNPQRSTVWXY]", re.IGNORECASE
    )
    just_digits = "SyntaxErrorJustDigits"
    reversed = "SyntaxErrorReverseAminoAcid"
    general = "SyntaxErrorGeneralModPos"
    for pos in positions:
        if re.fullmatch(main_pattern, pos) is None:
            formatted_string = (
                f"{pos} is not a valid modification position. "
                "Modification Position field should be a comma separated list of amino acid "
                "letters followed by position numbers (e.g. F1, S10, S300). "
            )

            if re.fullmatch(pattern=digits, string=pos):
                if int(pos) > len(pep_seq):
                    errors.append(
                        {
                            "level": "error",
                            "rule": just_digits,
                            "value": pos,
                            "field": "mod_pos",
                            "message": formatted_string + "This input is just digit(s)."
                            " Digit is bigger than length of peptide sequence",
                            "suggestion": None,
                        }
                    )
                else:
                    errors.append(
                        {
                            "level": "error",
                            "rule": just_digits,
                            "suggestion": str(pep_seq[int(pos) - 1] + pos),
                            "value": pos,
                            "field": "mod_pos",
                            "message": formatted_string
                            + "Enter amino acid before digit(s). ",
                        }
                    )

            elif re.fullmatch(pattern=reversed_pattern, string=pos):
                errors.append(
                    {
                        "level": "error",
                        "rule": reversed,
                        "suggestion": f"{pos[-1]}{pos[:-1]}",
                        "value": pos,
                        "field": "mod_pos",
                        "message": formatted_string
                        + "Enter amino acid followed by position.",
                    }
                )

            else:
                errors.append(
                    {
                        "level": "error",
                        "rule": general,
                        "value": pos,
                        "field": "mod_pos",
                        "message": formatted_string,
                        "suggestion": None,
                    }
                )
    return errors


def validate_peptide(pep_seq, mod_pos=None, mod_type=None):
    """Main helper function to validate, checks for validation of peptide sequence, modification
    position, and modification type"""
    errors = []
    errors.extend(validate_amino_acids(pep_seq))
    if mod_pos and mod_type:
        errors.extend(validate_modification(pep_seq, mod_pos, mod_type))
    return errors


def validate_modification(pep_seq, mod_pos, mod_type):
    errors = []
    positions, mod_types = format_mod_info(mod_pos, mod_type)
    mod_types = mod_types.split(",")
    errors.extend(validate_PTM_names(mod_types))
    errors.extend(validate_mod_pos_syntax(pep_seq, positions))
    if errors:
        return errors
    positions = positions.split(",")
    num_mod_types = len(mod_types)
    num_mod_pos = len(positions)
    mod_num_mismatch = "MismatchErrorNumModPosType"
    num_mistmatch_str = (
        f"There are {num_mod_pos} modification positions entered, but {num_mod_types} modification"
        " types. Number of modification positions is less than number of modification types. "
    )
    if num_mod_pos < num_mod_types:
        errors.append(
            {
                "level": "warn",
                "rule": mod_num_mismatch,
                "value": mod_pos,
                "field": "mod_pos",
                "message": num_mistmatch_str + " Decrease number of modification types"
                " or increase number of modification positions.",
                "suggestion": None,
            }
        )
    if num_mod_types < num_mod_pos:
        errors.append(
            {
                "level": "warn",
                "rule": mod_num_mismatch,
                "value": mod_type,
                "field": "mod_type",
                "message": num_mistmatch_str
                + " Decrease number of modification positions"
                " or increase number of modification types.",
                "suggestion": None,
            }
        )

    if errors:
        for error in errors:
            if (
                error["rule"] == "SyntaxErrorJustDigits"
                or error["rule"] == "SyntaxErrorReverseAminoAcid"
            ):
                positions.remove(error["value"])
            if error["rule"] == "SyntaxErrorGeneralModPos":
                return errors

    errors.extend(validate_mod_pos(pep_seq, positions))
    return errors


def validate_mhc_name(mhc_name):
    """Check if given MHC name match up to MRO name"""
    errors = []
    invalid_MHC_rule = "UndefinedArgMHCMol"
    if mhc_name not in molecules:
        errors.append(
            {
                "level": "error",
                "rule": invalid_MHC_rule,
                "value": mhc_name,
                "field": "mhc_name",
                "message": "Invalid entry in MHC molecule field."
                " Please use MHC molecule names as cataloged in MRO.",
                "suggestion": None,
            }
        )
    return errors


def validate_mod_pos(pep_seq, positions):
    """Validates the list of modification positions (in proper syntax) for peptide sequence entered
    as occuring at the stated position."""
    errors = []
    pos_pep_seq_rule = "MismatchErrorAminoAcidPos"
    try:
        for pos in positions:
            if len(pos) >= 2:
                position = "".join(pos[1:])
                position = int(position) - 1
                if pep_seq[position].upper() != pos[0].upper():
                    part_one = "This peptide sequence "
                    part_two = (
                        f"does not contain {pos[0].upper()} at position {pos[1:]}. "
                    )
                    result = part_one + part_two
                    errors.append(
                        {
                            "level": "error",
                            "rule": pos_pep_seq_rule,
                            "value": pos,
                            "field": "mod_pos",
                            "message": result
                            + "Enter a amino acid letter and matching position from peptide"
                            " sequence.",
                            "suggestion": None,
                        }
                    )

    except IndexError:
        index_rule = "MismatchErrorPosGreaterPepLen"
        formatted_string = (
            f"IndexError. {position + 1} is greater than number of"
            " amino acids in peptide sequence. "
        )
        errors.append(
            {
                "level": "error",
                "rule": index_rule,
                "value": int(pos[1:]),
                "field": "mod_pos",
                "message": formatted_string
                + "Enter position that is less than length of peptide sequence and more than 0.",
                "suggestion": None,
            }
        )
    return errors
