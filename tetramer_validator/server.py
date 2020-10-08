from flask import Flask
from flask import (
    render_template,
    request,
    send_from_directory,
    redirect,
    flash,
    send_file,
    url_for
)
from tetramer_validator import validate
from werkzeug.utils import secure_filename
from tetramer_validator.parse_tables import (
    parse_excel_file,
    parse_csv_tsv,
    generate_messages_txt,
    generate_formatted_data,
)
import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
import zipfile as zip

app = Flask(__name__)


ALLOWED_EXTENSIONS = {"csv", "tsv", "xlsx"}


app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            #flash("No file part")
            return redirect(url_for("output"))
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            #flash("No selected file")
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
    output = zip.ZipFile(file=zipped, mode="x", compression=zip.ZIP_DEFLATED)
    output.write(filename=path, arcname=os.path.split(path)[1])
    output.write(filename=errors_obj.name, arcname=os.path.split(errors_obj.name)[1])
    output.close()
    return send_file(zipped.name)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def output():
    if request.args:
        pep_seq = request.args["pep_seq"]
        mod_pos = request.args["mod_pos"]
        mod_type = request.args["mod_type"]
        mhc_name = request.args["mhc_name"]
        errors = validate.validate(
            pep_seq=pep_seq, mod_pos=mod_pos, mod_type=mod_type, mhc_name=mhc_name
        )
        success = not errors
        return render_template(
            "base.html",
            pep_seq=pep_seq,
            mod_pos=mod_pos,
            mod_type=mod_type,
            mhc_name=mhc_name,
            errors=errors,
            PTM_display=validate.PTM_display,
            success=success,
        )
    else:
        return render_template(
            "base.html",
            pep_seq="",
            mod_pos="",
            mod_type="",
            mhc_name="",
            PTM_display=validate.PTM_display,
            errors="",
            success=False,
        )


@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")


@app.route("/data/<path:filename>")
def send_js(filename):
    return send_from_directory("data", filename=filename)
