from tetramer_validator.validate import validate, validate_mod_pos


def test_validate_one():
    assert (
        validate(
            pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="K5", mod_type="OX"
        )
        == "MismatchError: This peptide sequence NLVPMVATV does not contain K at position 5"
    )


def test_validate_two():
    assert (
        validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="M5")
        == "Modificiation position provided but no modification type"
    )


def test_mod_pos_val_one():
    assert validate_mod_pos(pep_seq="NLVPMVATV", positions=["M5"]) is None


def test_mod_pos_val_two():
    assert (
        validate_mod_pos(pep_seq="NLVPMVATV", positions=["K5"])
        == "MismatchError: This peptide sequence NLVPMVATV does not contain K at position 5"
    )


def test_mod_pos_val_three():

    assert (
        validate_mod_pos(pep_seq="NLVPOVATV", positions=["M5"])
        == "MismatchError: This peptide sequence NLVPOVATV does not contain M at position 5"
    )


def test_mod_pos_val_four():
    system_err_pre = "Here is the error message from the system: "
    formatted_string = (
        "IndexError. 100 is greater than number of amino acids in"
        " peptide sequence NLVPOVATV."
    )
    final_string = (
        formatted_string + "\n" + system_err_pre + "string index out of range"
    )
    assert validate_mod_pos(pep_seq="NLVPOVATV", positions=["M100"]) == final_string
