from tetramer_validator.server import build_valid_multimers_strings
from tetramer_validator.validate import validate

# recreating rows list like in output function of server.py
def create_input_list(args):
    error_list = validate(
        mhc_name=args["mhc_name"],
        pep_seq=args["pep_seq"],
        mod_type=args["mod_type"],
        mod_pos=args["mod_pos"],
    )
    errors = {}
    for error in error_list:
        if error["field"] in errors:
            errors[error["field"]].append(error["message"])
        else:
            errors[error["field"]] = [error["message"]]
    success = []
    for key in args:
        if key not in errors:
            success.append(key)
    args["errors"] = errors
    args["success"] = success
    return args


# One valid and one invalid multimer entry
def test_build_valid_multimer_strings_one():
    args_1 = {
        "mhc_name": "HLA-A*01:01",
        "pep_seq": "NLVPPP",
        "mod_type": "oxidized residue",
        "mod_pos": "N1, P2",
    }
    args = [create_input_list(args_1)]
    args_2 = {
        "mhc_name": "HLA-A*01:01",
        "pep_seq": "NLVP",
        "mod_type": "oxidized residue, amidated residue",
        "mod_pos": "N1, P4",
    }
    args.append(create_input_list(args_2))
    assert (
        build_valid_multimers_strings(args)
        == "Tet1: HLA-A*01:01, NLVP + oxidized residue, amidated residue (N1, P4)"
    )


# Two invalid multimer entries
def test_build_valid_multimer_strings_two():
    args_1 = {
        "mhc_name": "HLA-A*01:01",
        "pep_seq": "NLVPPP",
        "mod_type": "oxidized residue",
        "mod_pos": "N1, P2",
    }
    args = [create_input_list(args_1)]
    args_2 = {
        "mhc_name": "HLA-A*01:01",
        "pep_seq": "NLVP",
        "mod_type": "oxidized residue, amidated residue",
        "mod_pos": "N1, P3",
    }
    args.append(create_input_list(args_2))
    assert build_valid_multimers_strings(args) == ""


# Two valid multimer entries
def test_build_valid_multimer_strings_three():
    args_1 = {
        "mhc_name": "HLA-A*01:01",
        "pep_seq": "NLVATY",
        "mod_type": "dehydrated residue",
        "mod_pos": "T5",
    }
    args = [create_input_list(args_1)]
    args_2 = {
        "mhc_name": "H2-Db",
        "pep_seq": "NLMMY",
        "mod_type": "acetylated residue",
        "mod_pos": "M4",
    }
    args.append(create_input_list(args_2))
    assert (
        build_valid_multimers_strings(args)
        == "Tet1: HLA-A*01:01, NLVATY + dehydrated residue (T5)\nTet2: H2-Db, NLMMY + acetylated residue (M4)"
    )
