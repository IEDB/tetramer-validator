from tetramer_validator.validate import validate_mhc_name


def test_validate_mhc_name_one():
    assert validate_mhc_name(mhc_name="HLA-A*02:01") == []


def test_validate_mhc_name_two():
    assert validate_mhc_name(mhc_name="HLA-A2") == [
        {
            "level": "error",
            "rule_name": "UndefinedMHCMol",
            "value": "HLA-A2",
            "field": "mhc_name",
            "instructions": "Enter MHC molecule from prepopulated list",
            "fix": None,
        }
    ]
