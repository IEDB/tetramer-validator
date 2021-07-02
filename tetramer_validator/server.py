from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    send_file,
    url_for,
)
from tetramer_validator import validate
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename
from openpyxl import Workbook

from tetramer_validator.parse_tables import (
    parse_excel_file,
    parse_csv_tsv,
    generate_messages_txt,
    generate_formatted_data,
)
import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
import itertools
import zipfile

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"csv", "tsv", "xlsx"}


app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


if not os.path.isdir("./downloads"):
    os.mkdir("./downloads")


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
            row["success"] = list(set(keys) - set(errors.keys()))
            row["pep_seq"] = row["pep_seq"].upper()
        if len(rows) == 0 or "add" in args:
            rows.append(
                {
                    "pep_seq": "",
                    "mod_pos": "",
                    "mod_type": "",
                    "mhc_name": "",
                    "errors": {},
                    "success": [],
                }
            )
        free_text = build_valid_multimers_strings(rows)
        return render_template("base.html", args=args, rows=rows, free_text=free_text)
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
                    "success": [],
                }
            ],
        )


def build_valid_multimers_strings(inputs):
    x = 0
    valid_multimers = []
    for input in inputs:
        # Check whether there is either mod_pos, mod_type, pep_seq, and mhc_name
        # or pep_seq and mhc_name
        if not bool(input["errors"]) and len(input["success"]) > 1:
            x = x + 1
            if input["mod_pos"] and input["mod_type"]:
                types = input["mod_type"].strip().replace(", ", ",").split(",")
                positions = input["mod_pos"].strip().replace(", ", ",").split(",")
                type_pos = tuple(zip(types, positions))
                type_pos = [f"{type} ({pos})" for type, pos in type_pos]
                type_pos = ", ".join(type_pos)
                valid_multimers.append(
                    f"Tet{x}: {input['mhc_name']}, {input['pep_seq']} + {type_pos}"
                )
            else:
                valid_multimers.append(
                    f"Tet{x}: {input['mhc_name']}, {input['pep_seq']}"
                )

    return "\n".join(valid_multimers)


def generate_file(input, errors):
    with NamedTemporaryFile(
        prefix="your_input_", suffix=".xlsx", dir="./downloads", delete=False
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
        return input_obj.name


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
        filename_or_fp=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        attachment_filename="your_input.xlsx",
    )


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            # flash("No file part")
            return redirect(url_for("output"))
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            # flash("No selected file")
            return redirect(url_for("output"))
        if file and allowed_file(file.filename):
            temp_dir = TemporaryDirectory(prefix="upload", suffix="")
            app.config["UPLOAD_FOLDER"] = temp_dir.name
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            return results(path)
    return ""


def results(path):
    errors = []
    any_errors = False
    if path.endswith("csv"):
        errors, any_errors = parse_csv_tsv(path, delimiter=",")
    elif path.endswith("tsv"):
        errors, any_errors = parse_csv_tsv(path, delimiter="\t")
    else:
        errors, any_errors = parse_excel_file(path)
        generate_formatted_data(path, errors)
    errors_obj = NamedTemporaryFile(
        mode="w",
        prefix="errors",
        suffix=".csv",
        dir=app.config["UPLOAD_FOLDER"],
        delete=False,
    )
    generate_messages_txt(messages=errors, file_obj=errors_obj)
    zipped = NamedTemporaryFile(
        prefix="output", suffix=".zip", dir=app.config["UPLOAD_FOLDER"], delete=False
    )
    output = zipfile.ZipFile(file=zipped, mode="x", compression=zipfile.ZIP_DEFLATED)
    output.write(filename=path, arcname=os.path.split(path)[1])
    output.write(filename=errors_obj.name, arcname="errors.csv")
    output.close()
    return send_file(
        filename_or_fp=zipped.name,
        mimetype="application/zip",
        as_attachment=True,
        attachment_filename="output.zip",
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
