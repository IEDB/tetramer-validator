import valve
import re

# Match peptide sequence with modification position
def validate_pep_seq_mod_pos_match(config, args, table, column, row_idx, value):
    messages = []
    rows = config["table_details"][table]
    row = rows["rows"][row_idx]
    pep_seq = row[args[0]["value"]]
    if not re.match("^[ACDEFGHIKLMNPQRSTVWXY][0-9]*$", value):
        messages.append(valve.error(config, table, column, row_idx, f"Incorrect Modification Position {value}. Must be a amino acid followed by a position in the peptide sequence."))
        return messages
    if pep_seq[int("".join(value[1:])) - 1] != value[0]:
        message = valve.error(config, table, column, row_idx, f"{value[0]} is not the amino acid at position {value[1]}")
        messages.append(message)
    return messages


def validate_len_compare(config, args, table, column, row_idx, value):
    messages = []
    mod_types = value.split(",")
    len_mod_types = len(mod_types)
    len_mod_pos = len(config["table_details"][table]["rows"][row_idx][args[0]["value"]].split(","))
    if len_mod_types != len_mod_pos:
        message = f"Number of positions, {len_mod_pos} does not match number of modification types, {len_mod_types}"
        messages.append(valve.error(config, table, column, row_idx, message))
    return messages
valve.write_messages("report.tsv", valve.validate(["valve_tetramers/"], add_functions = {"len_compare": {"check": ["column"],"validate": validate_len_compare} , "pep_seq_mod_pos_match": {"check":["column"],"validate": validate_pep_seq_mod_pos_match}} ))
