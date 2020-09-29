from tetramer_validator.validate import properNumArguments


def test_properNumArguments_one():
    assert properNumArguments(
        {"pep_seq": "NLVPMVATV", "mod_pos": "M5", "mhc_name": "HLA", "mod_type": ""}
    ) == [
        {
            "level": "error",
            "rule_name": "IncorrectNumArgs" + "ModType",
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
            "rule_name": "IncorrectNumArgs" + "ModPos",
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
            "rule_name": "IncorrectNumArgs" + "PepSeq",
            "value": "",
            "field": "pep_seq",
            "instructions": "Enter peptide sequence.",
            "fix": None,
        }
    ]
