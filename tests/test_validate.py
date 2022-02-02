from tetramer_validator.validate import (
    validate,
    validate_amino_acids,
    validate_mod_pos,
    validate_peptide,
    validate_PTM_names,
    validate_mod_pos_syntax,
    properNumArguments,
    validate_mhc_name,
)

# Uncomment after synonyms has been implemented
# def test_validate_one():
#    assert (
#        validate(
#            pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="K5", mod_type="OX"
#        )
#        == "MismatchError: This peptide sequence NLVPMVATV does not contain K at position 5"
#    )


def test_validate_one():
    assert validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01") == []


def test_validate_PTM_names_one():
    assert validate_PTM_names(["oxidized"]) == [
        {
            "level": "error",
            "rule": "UndefinedArgPTMtype",
            "value": "oxidized",
            "message": "Invalid entry for post-translational modification type."
            " Please use post-translational modification type as cataloged in PSI-MOD.",
            "field": "mod_type",
            "suggestion": None,
        }
    ]


def test_validate_PTM_names_two():
    assert validate_PTM_names(["oxidized residue"]) == []


def test_validate_PTM_names_three():
    assert validate_PTM_names(["ox"]) == [
        {
            "level": "error",
            "rule": "ModTypeSynonymError",
            "value": "ox",
            "message": f"ox is a lower case string for OX.",
            "field": "mod_type",
            "suggestion": "oxidized residue",
        }
    ]


def test_validate_PTM_names_four():
    assert validate_PTM_names(["OX"]) == [
        {
            "level": "error",
            "rule": "ModTypeSynonymError",
            "value": "OX",
            "field": "mod_type",
            "message": f"OX is a synonym for oxidized residue.",
            "suggestion": "oxidized residue",
        }
    ]


def test_validate_amino_acids_one():
    assert validate_amino_acids(pep_seq="NLBPMVATV") == [
        {
            "level": "error",
            "rule": "UndefinedArgAminoAcid",
            "value": "NLBPMVATV",
            "field": "pep_seq",
            "message": "The peptide sequence has characters ['B']"
            " that are not amino acids. Please remove them.",
            "suggestion": None,
        }
    ]


def test_validate_amino_acids_two():
    assert validate_amino_acids(pep_seq="NLPMVATV") == []


def test_validate_mhc_name_one():
    assert validate_mhc_name(mhc_name="HLA-A*02:01") == []


def test_validate_mhc_name_two():
    assert validate_mhc_name(mhc_name="HLA-A2") == [
        {
            "level": "error",
            "rule": "UndefinedArgMHCMol",
            "value": "HLA-A2",
            "field": "mhc_name",
            "message": "Invalid entry in MHC molecule field."
            " Please use MHC molecule names as cataloged in MRO.",
            "suggestion": None,
        }
    ]


def test_validate_mod_pos_one():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["M5"]) == []


def test_validate_mod_pos_two():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["K5"]) == [
        {
            "level": "error",
            "rule": "MismatchErrorAminoAcidPos",
            "value": "K5",
            "message": "This peptide sequence does not contain K at position 5."
            " Enter a amino acid letter and matching position from peptide sequence.",
            "field": "mod_pos",
            "suggestion": None,
        }
    ]


def test_validate_mod_pos_three():

    assert validate_mod_pos(pep_seq="NMLVPOVATV", positions=["M5"]) == [
        {
            "level": "error",
            "rule": "MismatchErrorAminoAcidPos",
            "value": "M5",
            "message": "This peptide sequence does not contain M at position 5."
            " Enter a amino acid letter and matching position from peptide sequence.",
            "field": "mod_pos",
            "suggestion": None,
        }
    ]


def test_valdate_mod_pos_four():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["M100"]) == [
        {
            "level": "error",
            "rule": "MismatchErrorPosGreaterPepLen",
            "value": 100,
            "message": "IndexError. 100 is greater than number of amino acids in"
            " peptide sequence."
            " Enter position that is less than length of peptide sequence and more than 0.",
            "field": "mod_pos",
            "suggestion": None,
        }
    ]


def test_validate_mod_pos_five():
    assert validate_mod_pos(
        pep_seq="SILKIHAREIFDSRG",
        positions=["S1", "A7", "S10"],
    ) == [
        {
            "level": "error",
            "rule": "MismatchErrorAminoAcidPos",
            "value": "S10",
            "message": "This peptide sequence does not contain S at position 10."
            " Enter a amino acid letter and matching position from peptide sequence.",
            "field": "mod_pos",
            "suggestion": None,
        }
    ]


def test_validate_mod_pos_syntax_one():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions="5") == [
        {
            "level": "error",
            "rule": "SyntaxErrorJustDigits",
            "value": "5",
            "message": "5 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letters"
            " followed by position numbers (e.g. F1, S10, S300). Enter amino acid before"
            " digit(s). ",
            "field": "mod_pos",
            "suggestion": "M5",
        }
    ]


def test_validate_mod_pos_syntax_two():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions="5,1") == [
        {
            "level": "error",
            "rule": "SyntaxErrorJustDigits",
            "value": "5",
            "message": "5 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letters"
            " followed by position numbers (e.g. F1, S10, S300). Enter amino acid before"
            " digit(s). ",
            "field": "mod_pos",
            "suggestion": "M5",
        },
        {
            "level": "error",
            "rule": "SyntaxErrorJustDigits",
            "value": "1",
            "message": "1 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letters"
            " followed by position numbers (e.g. F1, S10, S300). Enter amino acid before"
            " digit(s). ",
            "field": "mod_pos",
            "suggestion": "N1",
        },
    ]


def test_validate_mod_pos_syntax_three():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions="1N") == [
        {
            "level": "error",
            "rule": "SyntaxErrorReverseAminoAcid",
            "value": "1N",
            "message": "1N is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letters"
            " followed by position numbers (e.g. F1, S10, S300). Enter amino acid followed"
            " by position.",
            "field": "mod_pos",
            "suggestion": "N1",
        }
    ]


def test_validate_mod_pos_syntax_four():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions="90") == [
        {
            "level": "error",
            "rule": "SyntaxErrorJustDigits",
            "value": "90",
            "message": "90 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letters"
            " followed by position numbers (e.g. F1, S10, S300). "
            "This input is just"
            " digit(s). "
            "Digit is bigger than length of peptide sequence.",
            "field": "mod_pos",
            "suggestion": None,
        }
    ]


def test_validate_mod_pos_syntax_five():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions="A1/A2") == [
        {
            "level": "error",
            "rule": "SyntaxErrorGeneralModPos",
            "value": "A1/A2",
            "message": "A1/A2 is not a valid modification position. Modification Position "
            "field should be a comma separated list of amino acid letters followed by position"
            " numbers "
            "(e.g. F1, S10, S300). ",
            "field": "mod_pos",
            "suggestion": None,
        }
    ]


def test_validate_mod_pos_syntax_six():
    assert validate_mod_pos_syntax(pep_seq="fff", positions="mra") == [
        {
            "level": "error",
            "rule": "SyntaxErrorGeneralModPos",
            "value": "mra",
            "field": "mod_pos",
            "message": "mra is not a valid modification position. Modification Position "
            "field should be a comma separated list of amino acid letters followed by position"
            " numbers (e.g. F1, S10, S300). ",
            "suggestion": None,
        }
    ]


def test_validate_mod_pos_syntax_seven():
    assert validate_mod_pos_syntax(pep_seq="fff", positions="0F") == [
        {
            "level": "error",
            "rule": "SyntaxErrorReverseAminoAcidZeroIndex",
            "value": "0F",
            "field": "mod_pos",
            "message": f"0F is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid "
            + "letters followed by position numbers (e.g. F1, S10, S300). "
            + "Zero-based indexing is not allowed. "
            + "Enter amino acid followed by position.",
            "suggestion": "f1",
        }
    ]


def test_validate_mod_pos_syntax_eight():
    assert validate_mod_pos_syntax(pep_seq="aff", positions="0F") == [
        {
            "level": "error",
            "rule": "SyntaxErrorReverseAminoAcidZeroIndex",
            "value": "0F",
            "field": "mod_pos",
            "message": f"0F is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid "
            + "letters followed by position numbers (e.g. F1, S10, S300). "
            + "Zero-based indexing is not allowed. "
            + "Enter amino acid followed by position.",
            "suggestion": "a1",
        }
    ]


def test_validate_mod_pos_syntax_nine():
    assert validate_mod_pos_syntax(pep_seq="fff", positions="F0") == [
        {
            "level": "error",
            "rule": "SyntaxErrorZeroIndex",
            "value": "F0",
            "field": "mod_pos",
            "message": f"F0 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid "
            + "letters followed by position numbers (e.g. F1, S10, S300). "
            + "Zero-based indexing is not allowed. ",
            "suggestion": "f1",
        }
    ]


def test_validate_mod_pos_syntax_ten():
    assert validate_mod_pos_syntax(pep_seq="aff", positions="F0") == [
        {
            "level": "error",
            "rule": "SyntaxErrorZeroIndex",
            "value": "F0",
            "field": "mod_pos",
            "message": f"F0 is not a valid modification position. "
            + "Modification Position field should be a comma separated list of amino acid "
            + "letters followed by position numbers (e.g. F1, S10, S300). "
            + "Zero-based indexing is not allowed. ",
            "suggestion": "a1",
        }
    ]


def test_validate_mod_pos_syntax_eleven():
    assert validate_mod_pos_syntax(pep_seq="aff", positions="0") == [
        {
            "level": "error",
            "rule": "SyntaxErrorJustDigitsZeroIndex",
            "value": "0",
            "field": "mod_pos",
            "message": f"0 is not a valid modification position. "
            + "Modification Position field should be a comma separated list of amino acid "
            + "letters followed by position numbers (e.g. F1, S10, S300). "
            + "Zero-based indexing is not allowed. "
            + "Enter amino acid before digit(s). ",
            "suggestion": "a1",
        }
    ]


def test_validate_peptide_one():
    assert validate_peptide(
        pep_seq="NLVPMVATV",
        mod_pos="N1, N2,uddssdagvfuad",
        mod_type="oxidized residue",
    ) == [
        {
            "level": "error",
            "rule": "SyntaxErrorTrailingCharacters",
            "value": "N1,N2,uddssdagvfuad",
            "field": "mod_pos",
            "message": "Syntax error in Modification Position field."
            " Remove ',uddssdagvfuad' from Modification Position.",
            "suggestion": None,
        }
    ]


def test_validate_peptide_two():
    assert validate_peptide(
        pep_seq="NLVPMVATV", mod_pos="N1, L2", mod_type="amidated residue"
    ) == [
        {
            "level": "warn",
            "rule": "MismatchErrorNumModPosType",
            "value": "amidated residue",
            "message": "There are 2 modification positions entered, but 1 modification types. "
            "Number of modification positions is less than number of modification types.  "
            "Decrease number of modification positions or increase number of "
            "modification types.",
            "field": "mod_type",
            "suggestion": None,
        }
    ]


def test_validate_peptide_three():
    assert validate_peptide(
        pep_seq="MMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
        mod_pos="M6,M6,M6",
        mod_type="formylated residue,formylated residue,formylated residue",
    ) == [
        {
            "level": "warn",
            "rule": "DupModPos",
            "value": "M6",
            "message": "M6 with same modification type formylated residue "
            "appears more than once in modification positions.",
            "field": "mod_pos",
            "suggestion": None,
        }
    ]


def test_properNumArguments_one():
    assert properNumArguments(
        {"pep_seq": "NLVPMVATV", "mod_pos": "M5", "mhc_name": "HLA", "mod_type": ""}
    ) == [
        {
            "level": "error",
            "rule": "IncorrectNumArgs" + "ModType",
            "value": "",
            "field": "mod_type",
            "message": "Modification position is filled, but modification type is not."
            " Provide modificiation type(s).",
            "suggestion": None,
        }
    ]


def test_properNumArguments_two():
    assert properNumArguments(
        {
            "pep_seq": "NLVPMVATV",
            "mod_type": "amidated residue",
            "mhc_name": "HLA",
            "mod_pos": "",
        }
    ) == [
        {
            "level": "error",
            "rule": "IncorrectNumArgs" + "ModPos",
            "value": "",
            "field": "mod_pos",
            "message": "Modification type is filled, but modification position is not."
            " Provide modificiation position(s).",
            "suggestion": None,
        }
    ]


def test_properNumArguments_three():
    assert properNumArguments(
        {
            "pep_seq": "",
            "mod_pos": "N1",
            "mod_type": "oxidized residue",
            "mhc_name": "HLA",
        }
    ) == [
        {
            "level": "error",
            "rule": "IncorrectNumArgs" + "PepSeq",
            "value": "",
            "field": "pep_seq",
            "message": "Peptide sequence missing. Enter peptide sequence.",
            "suggestion": None,
        }
    ]
