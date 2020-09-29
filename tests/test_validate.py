from tetramer_validator.validate import validate

# Uncomment after synonyms has been implemented
# def test_validate_one():
#    assert (
#        validate(
#            pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01", mod_pos="K5", mod_type="OX"
#        )
#        == "MismatchError: This peptide sequence NLVPMVATV does not contain K at position 5"
#    )


def test_validate_one():
    assert validate(pep_seq="NLVPMVATV", mhc_name="HLA-A*02:01") == []


# def test_validate_four():
#     assert (
#         validate(
#             pep_seq="NLV",
#             mhc_name="HLA-A&02:01",
#             mod_pos="NULL",
#             mod_type="oxidized residue",
#         )
#         == "NULL value entered. If there is no need for a particular value, please leave blank."
#     )
