from tetramer_validator.validate import validate_peptide


def test_validate_peptide_one():
    assert validate_peptide(
        pep_seq="NLVPMVATV",
        mod_pos="N1, N2,uddssdagvfuad",
        mod_type="oxidized residue",
    ) == [
        {
            "level": "error",
            "rule_name": "FormatErrorTrailingCharacters",
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
            "rule_name": "MismatchErrorNumModPosType",
            "value": "amidated residue",
            "instructions": "Decrease number of modification positions or increase number of modification types",
            "field": "mod_type",
            "fix": None,
        }
    ]
