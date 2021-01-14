import valve
import re

# Match peptide sequence with modification position
def validate_pep_seq_mod_pos_match(config, args, table, column, row_idx, value):
    messages = []

    rows = config["table_details"][table]
    print(args)
    row = rows["rows"][row_idx]
    pep_seq = row[args[0]["value"]]
    if not re.match("/^[ACDEFGHIKLMNPQRSTVWXY][0-9]*$/", value):
        messages.append(valve.error(config, table, column, row_idx, "Incorrect Modification Position. Must be a amino acid followed by a position in the peptide sequence."))
        return messages
    if pep_seq[int("".join(value[1:])) - 1] != value[0]:
        message = valve.error(config, table, column, row_idx, message1)
        messages.append(message)
    return messages


def validate_len_compare(config, args, table, column, row_idx, value):
    messages = []
    x = value.split(",")
    len_value = len(x)
    if len_value != config["table_details"][table]["rows"][row_idx][args[0]["value"]]:
        message = "Number of positions does not match number of modification types"
        messages.append(valve.error(config, table, column, row_idx, message))
    return messages
valve.write_messages("report.tsv", valve.validate(["valve_tetramers/"], add_functions = {"len_compare": {"check": ["column"],"validate": validate_len_compare} , "pep_seq_mod_pos_match": {"check":["column"],"validate": validate_pep_seq_mod_pos_match}} ))
