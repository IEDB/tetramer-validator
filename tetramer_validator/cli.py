import argparse
from tetramer_validator.parse_tables import (
    parse_csv_tsv,
    parse_excel_file,
    generate_messages_txt,
)
import tetramer_validator.server as server


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Options for use")
    subparsers = parser.add_subparsers(dest="subparser")
    parse_web = subparsers.add_parser(
        "webserver", help="Options for deploying tool as webserver"
    )
    parse_web.add_argument(
        "--host",
        default="127.0.0.1",
        help="If this option is not specified, host will default to 127.0.0.1",
    )
    parse_web.add_argument(
        "--port",
        type=int,
        default=5000,
        help="If this option is not specified, port will default to 5000",
    )
    parse_web.add_argument(
        "--debug",
        action="store_true",
        help="Option used to specify if Flask server should start in debug mode",
    )
    file_help_text = """Please enter .tsv, .csv, or .xlsx filename
        and that the following is in the header row:
        Peptide Sequence, Modification Type, Modification Position, MHC Molecule"""
    out_help_text = "Enter output file text name."
    parse_cmd = subparsers.add_parser(
        "cmd_line", help="Option to run validator on files through command line"
    )
    parse_cmd.add_argument("filename", help=file_help_text)
    parse_cmd.add_argument("-o", "--output", required=False, help=out_help_text)

    args = parser.parse_args()
    if args.subparser == "cmd_line":
        filename = args.filename
        output_file = args.output
        messages = []
        any_error = False
        if filename.endswith(".tsv"):
            messages, any_error = parse_csv_tsv(filename, delimiter="\t")
        elif filename.endswith(".csv"):
            messages, any_error = parse_csv_tsv(filename, delimiter=",")
        elif filename.endswith(".xlsx"):
            messages, any_error = parse_excel_file(filename)
        else:
            print("Sorry, file is not valid format. Must be .tsv, .csv, or .xlsx file")
            sys.exit(1)
        if any_error:
            if output_file:
                file_obj = open(output_file, "w")
                generate_messages_txt(messages, file_obj)
            else:
                for message in messages:
                    print(message)
        return sys.exit(any_error)
    if args.subparser == "webserver":
        server.app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
