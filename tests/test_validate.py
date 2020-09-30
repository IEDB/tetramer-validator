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
            "rule name": "UndefinedArgPTMtype",
            "value": "oxidized",
            "instructions": "Please choose a post-translational type from the prepopulated list.",
            "field": "mod_type",
            "fix": None,
        }
    ]


def test_validate_PTM_names_two():
    assert validate_PTM_names(["oxidized residue"]) == []


def test_validate_amino_acids_one():
    assert validate_amino_acids(pep_seq="NLBPMVATV") == [
        {
            "level": "error",
            "rule name": "UndefinedArgAminoAcid",
            "value": "NLBPMVATV",
            "field": "pep_seq",
            "instructions": "The peptide sequence has characters ['B']"
            " that are not amino acids",
            "fix": None,
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
            "rule name": "UndefinedMHCMol",
            "value": "HLA-A2",
            "field": "mhc_name",
            "instructions": "Enter MHC molecule from prepopulated list",
            "fix": None,
        }
    ]


def test_validate_mod_pos_one():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["M5"]) == []


def test_validate_mod_pos_two():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["K5"]) == [
        {
            "level": "error",
            "rule name": "MismatchErrorAminoAcidPos",
            "value": "K5",
            "instructions": "This peptide sequence does not contain K at position 5."
            " Enter a amino acid letter and matching position from peptide sequence",
            "field": "mod_pos",
            "fix": None,
        }
    ]


def test_validate_mod_pos_three():

    assert validate_mod_pos(pep_seq="NMLVPOVATV", positions=["M5"]) == [
        {
            "level": "error",
            "rule name": "MismatchErrorAminoAcidPos",
            "value": "M5",
            "instructions": "This peptide sequence does not contain M at position 5."
            " Enter a amino acid letter and matching position from peptide sequence",
            "field": "mod_pos",
            "fix": None,
        }
    ]


def test_valdate_mod_pos_four():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["M100"]) == [
        {
            "level": "error",
            "rule name": "MismatchErrorPosGreaterPepLen",
            "value": 100,
            "instructions": "IndexError. 100 is greater than number of amino acids in peptide sequence."
            " Enter position that is less than length of peptide sequence and more than 0.",
            "field": "mod_pos",
            "fix": None,
        }
    ]


def test_validate_mod_pos_five():
    assert validate_mod_pos(
        pep_seq="SILKIHAREIFDSRG",
        positions=["S1", "A7", "S10"],
    ) == [
        {
            "level": "error",
            "rule name": "MismatchErrorAminoAcidPos",
            "value": "S10",
            "instructions": "This peptide sequence does not contain S at position 10."
            " Enter a amino acid letter and matching position from peptide sequence",
            "field": "mod_pos",
            "fix": None,
        }
    ]


def test_validate_mod_pos_syntax_one():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions=["5"]) == [
        {
            "level": "error",
            "rule name": "FormatErrorJustDigits",
            "value": "5",
            "instructions": "5 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letter"
            " followed by position number (e.g. F1, S10, S300). Enter amino acid before digit(s). ",
            "field": "mod_pos",
            "fix": "M5",
        }
    ]


def test_validate_mod_pos_syntax_two():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions=["5", "1"]) == [
        {
            "level": "error",
            "rule name": "FormatErrorJustDigits",
            "value": "5",
            "instructions": "5 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letter"
            " followed by position number (e.g. F1, S10, S300). Enter amino acid before digit(s). ",
            "field": "mod_pos",
            "fix": "M5",
        },
        {
            "level": "error",
            "rule name": "FormatErrorJustDigits",
            "value": "1",
            "instructions": "1 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letter"
            " followed by position number (e.g. F1, S10, S300). Enter amino acid before digit(s). ",
            "field": "mod_pos",
            "fix": "N1",
        },
    ]


def test_validate_mod_pos_syntax_three():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions=["1N"]) == [
        {
            "level": "error",
            "rule name": "FormatErrorReverseAminoAcid",
            "value": "1N",
            "instructions": "1N is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letter"
            " followed by position number (e.g. F1, S10, S300). Enter amino acid followed by position.",
            "field": "mod_pos",
            "fix": "N1",
        }
    ]


def test_validate_mod_pos_syntax_four():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions=["90"]) == [
        {
            "level": "error",
            "rule name": "FormatErrorJustDigits",
            "value": "90",
            "instructions": "90 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letter"
            " followed by position number (e.g. F1, S10, S300). This input is just digit(s). "
            "Digit is bigger than length of peptide sequence",
            "field": "mod_pos",
            "fix": None,
        }
    ]


def test_validate_mod_pos_syntax_five():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions=["A1/A2"]) == [
        {
            "level": "error",
            "rule name": "FormatErrorGeneralModPos",
            "value": "A1/A2",
            "instructions": "A1/A2 is not a valid modification position. Modification Position "
            "field should be a comma separated list of amino acid letter followed by position number "
            "(e.g. F1, S10, S300). ",
            "field": "mod_pos",
            "fix": None,
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
            "rule name": "FormatErrorTrailingCharacters",
            "value": "N1, N2,uddssdagvfuad",
            "field": "mod_pos",
            "instructions": "Remove [',uddssdagvfuad'] from modification position.",
            "fix": None,
        }
    ]


def test_validate_peptide_two():
    assert validate_peptide(
        pep_seq="NLVPMVATV", mod_pos="N1, L2", mod_type="amidated residue"
    ) == [
        {
            "level": "warn",
            "rule name": "MismatchErrorNumModPosType",
            "value": "amidated residue",
            "instructions": "Decrease number of modification positions or increase number of "
            "modification types",
            "field": "mod_type",
            "fix": None,
        }
    ]


def test_properNumArguments_one():
    assert properNumArguments(
        {"pep_seq": "NLVPMVATV", "mod_pos": "M5", "mhc_name": "HLA", "mod_type": ""}
    ) == [
        {
            "level": "error",
            "rule name": "IncorrectNumArgs" + "ModType",
            "value": "",
            "field": "mod_type",
            "instructions": "Provide modificiation type(s).",
            "fix": None,
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
            "rule name": "IncorrectNumArgs" + "ModPos",
            "value": "",
            "field": "mod_pos",
            "instructions": "Provide modificiation position(s).",
            "fix": None,
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
            "rule name": "IncorrectNumArgs" + "PepSeq",
            "value": "",
            "field": "pep_seq",
            "instructions": "Enter peptide sequence.",
            "fix": None,
        }
    ]
