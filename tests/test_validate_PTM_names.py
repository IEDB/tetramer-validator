from tetramer_validator.validate import validate_PTM_names


def test_validate_PTM_names_one():
    assert validate_PTM_names(["oxidized"]) == [
        {
            "level": "error",
            "rule_name": "UndefinedArgPTMtype",
            "value": "oxidized",
            "instructions": "Please choose a post-translational type from the prepopulated list",
            "field": "mod_type",
            "fix": None,
        }
    ]


def test_validate_PTM_names_two():
    assert validate_PTM_names(["oxidized residue"]) == []
