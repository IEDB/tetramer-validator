def test_validate_one():
    assert (
        validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="K5")
        == "This peptide sequence NLVPMVATV does not contain K at position 5"
    )


def test_validate_two():
    assert validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="M5") == None


def test_mod_pos_val_one():
    assert validate_mod_pos(pep_seq="NLVPMVATV", modifications=[("M", 5)]) == None


def test_mod_pos_val_two():
    assert (
        validate_mod_pos(pep_seq="NLVPMVATV", modifications=[("K", 5)])
        == "This peptide sequence NLVPMVATV does not contain K at position 5"
    )


def test_mod_pos_val_three():
    assert (
        validate_mod_pos(pep_seq="NLVPOVATV", modifications=[("M", 5)])
        == "This peptide sequence NLVPOVATV does not contain M at position 5"
    )
