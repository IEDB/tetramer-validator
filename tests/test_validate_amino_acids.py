from tetramer_validator.validate import validate_amino_acids


def test_validate_amino_acids_one():
    assert validate_amino_acids(pep_seq="NLBPMVATV") == [
        {
            "level": "error",
            "rule_name": "UndefinedArgAminoAcid",
            "value": "NLBPMVATV",
            "field": "pep_seq",
            "instructions": "The peptide sequence has characters ['B']"
            " that are not amino acids",
            "fix": None,
        }
    ]


def test_validate_amino_acids_two():
    assert validate_amino_acids(pep_seq="NLPMVATV") == []
