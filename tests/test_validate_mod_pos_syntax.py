from tetramer_validator.validate import validate_mod_pos_syntax


def test_validate_mod_pos_syntax_one():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions=["5"]) == [
        {
            "level": "error",
            "rule_name": "FormatErrorJustDigits",
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
            "rule_name": "FormatErrorJustDigits",
            "value": "5",
            "instructions": "5 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letter"
            " followed by position number (e.g. F1, S10, S300). Enter amino acid before digit(s). ",
            "field": "mod_pos",
            "fix": "M5",
        },
        {
            "level": "error",
            "rule_name": "FormatErrorJustDigits",
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
            "rule_name": "FormatErrorReverseAminoAcid",
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
            "rule_name": "FormatErrorJustDigits",
            "value": "90",
            "instructions": "90 is not a valid modification position. "
            "Modification Position field should be a comma separated list of amino acid letter"
            " followed by position number (e.g. F1, S10, S300). This input is just digit(s).  "
            "Digit is bigger than length of peptide sequence",
            "field": "mod_pos",
            "fix": None,
        }
    ]


def test_validate_mod_pos_syntax_five():
    assert validate_mod_pos_syntax(pep_seq="NLVPMVATV", positions=["A1/A2"]) == [
        {
            "level": "error",
            "rule_name": "FormatErrorGeneralModPos",
            "value": "A1/A2",
            "instructions": "A1/A2 is not a valid modification position. Modification Position "
            "field should be a comma separated list of amino acid letter followed by position number (e.g. F1, S10, S300). ",
            "field": "mod_pos",
            "fix": None,
        }
    ]
