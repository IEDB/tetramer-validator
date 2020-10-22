from flask import Flask
from flask import render_template, request, send_from_directory
from tetramer_validator import validate
from werkzeug.datastructures import MultiDict

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
                    error["message"] + " Suggested fix is " + error["suggestion"] +".",
                )
                for error in errors
            ]
            errors = MultiDict(errors)
            row["errors"] = errors.to_dict(False)
            row["success"] = list(set(keys) - set(errors.keys()))
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
                    "success": [],
                }
            ],
        )


@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")


@app.route("/data/<path:filename>")
def send_js(filename):
    return send_from_directory("data", filename=filename)
