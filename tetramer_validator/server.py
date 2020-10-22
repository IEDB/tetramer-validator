from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    send_file,
)
from tetramer_validator import validate
from werkzeug.datastructures import MultiDict
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
from tetramer_validator.parse_tables import generate_formatted_data
import itertools
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def output():
    if request.args:
        args = request.args.to_dict(flat=False)
        rows = []
        keys = ["mhc_name", "pep_seq", "mod_type", "mod_pos"]
        max_rows = 0
        for k in keys:
            if k in args:
                max_rows = max(max_rows, len(args[k]))
        args["max"] = max_rows
        for i in range(0, max_rows):
            row = {}
            for k in keys:
                if k in args and len(args[k]) > i:
                    row[k] = args[k][i]
            rows.append(row)
            errors = validate.validate(**row)
            row["success"] = not errors
            errors = [
                (error["field"], error["message"])
                if error["suggestion"] is None
                else (
                    error["field"],
                    error["message"] + " Suggested fix is " + error["suggestion"] + ".",
                )
                for error in errors
            ]
            errors = MultiDict(errors)
            row["errors"] = errors.to_dict(False)

        if len(rows) == 0 or "add" in args:
            rows.append(
                {
                    "pep_seq": "",
                    "mod_pos": "",
                    "mod_type": "",
                    "mhc_name": "",
                    "errors": {},
                    "success": False,
                }
            )
        return render_template(
            "base.html",
            args=args,
            rows=rows,
        )
    else:
        return render_template(
            "base.html",
            rows=[
                {
                    "pep_seq": "",
                    "mod_pos": "",
                    "mod_type": "",
                    "mhc_name": "",
                    "errors": {},
                    "success": False,
                }
            ],
        )


def generate_file(input, errors):
    with NamedTemporaryFile(
        prefix="your_input_", suffix=".xlsx", dir="static", delete=False
    ) as input_obj:
        input_data = Workbook()
        ws = input_data.active
        ws.append(
            (
                "MHC Molecule",
                "Peptide Sequence",
                "Modification Type",
                "Modification Position",
            )
        )
        for entry in input:
            ws.append(entry)
        input_data.save(input_obj.name)
        header_dict = {"mhc_name": "A", "pep_seq": "B", "mod_type": "C", "mod_pos": "D"}
        for input_num in errors.keys():
            errorlist = errors[input_num]
            list(
                map(
                    lambda error: error.update(
                        {"cell": header_dict[error["field"]] + str(input_num + 2)}
                    ),
                    errorlist,
                )
            )
        generate_formatted_data(
            input_obj.name, list(itertools.chain.from_iterable(errors.values()))
        )
        return os.path.split(input_obj.name)[1]


@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")


@app.route("/data/<path:filename>")
def send_data(filename):
    return send_from_directory("data", filename=filename)


@app.route("/downloads", methods=["GET"])
def download_input():
    input = request.args.to_dict(flat=False)
    errors = dict(
        enumerate(itertools.starmap(validate.validate, zip(*(input.values()))))
    )
    to_input = list(map(list, zip(*(input.values()))))
    filename = generate_file(to_input, errors)
    return send_file(
        filename_or_fp="static/" + str(filename),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        attachment_filename="your_input.xlsx",
    )
