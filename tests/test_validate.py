from tetramer_validator.validate import validate, validate_mod_pos

# Uncomment after synonyms has been implemented
# def test_validate_one():
#    assert (
#        validate(
#            pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="K5", mod_type="OX"
#        )
#        == "MismatchError: This peptide sequence NLVPMVATV does not contain K at position 5"
#    )


def test_validate_one():
    assert validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01") is None


def test_validate_two():
    assert (
        validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="M5")
        == "Incorrect combination of arguments: Modificiation position provided"
        " but no modification type"
    )


def test_validate_three():
    assert (
        validate(
            pep_seq="NLVPMVATV",
            mhc_name="HLA-A*02:01",
            mod_pos="K5",
            mod_type="oxidized residue",
        )
        == "MismatchError: This peptide sequence NLVPMVATV does not contain K at position 5"
    )


def test_validate_four():
    assert (
        validate(
            pep_seq="NLV",
            mhc_name="HLA-A&02:01",
            mod_pos="NULL",
            mod_type="oxidized residue",
        )
        == "NULL value entered. If there is no need for a particular value, please leave blank."
    )


def test_validate_five():
    assert (
        validate(pep_seq="", mod_pos="N1", mod_type="oxidized residue")
        == "Incorrect number of arguments: Peptide sequence is required"
    )


def test_validate_six():
    assert (
        validate(
            pep_seq="NLVPMVATV",
            mhc_name="HLA-A&02:0",
            mod_pos="N1, N2,uddssdagvfuad",
            mod_type="oxidized residue",
        )
        == "FormatError:"
        " [',uddssdagvfuad']"
        " at the end of input N1, N2,uddssdagvfuad"
        " are unrecognized"
    )


def test_validate_seven():
    assert (
        validate(
            pep_seq="SILKIHAREIFDSRG",
            mod_type="acetylated residue, L-citrylline, L-citrylline",
            mod_pos="S1, A7, S10",
        )
        == "MismatchError: This peptide sequence SILKIHAREIFDSRG does not contain S at position 10"
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
