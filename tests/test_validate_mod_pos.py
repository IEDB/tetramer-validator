from tetramer_validator.validate import validate_mod_pos


def test_validate_mod_pos_one():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["M5"]) == []


def test_validate_mod_pos_two():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["K5"]) == [
        {
            "level": "error",
            "rule_name": "MismatchErrorAminoAcidPos",
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
            "rule_name": "MismatchErrorAminoAcidPos",
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
            "rule_name": "MismatchErrorPosGreaterPepLen",
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
            "rule_name": "MismatchErrorAminoAcidPos",
            "value": "S10",
            "instructions": "This peptide sequence does not contain S at position 10."
            " Enter a amino acid letter and matching position from peptide sequence",
            "field": "mod_pos",
            "fix": None,
        }
    ]
