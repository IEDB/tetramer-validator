from flask import Flask
from flask import render_template, request, send_from_directory, redirect, flash, url_for, send_file
from tetramer_validator import validate, parse_tables
from werkzeug.utils import secure_filename
from tetramer_validator.parse_tables import parse_excel_file, parse_csv_tsv, generate_messages_txt
import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
import time
app = Flask(__name__)


ALLOWED_EXTENSIONS = {'csv', 'tsv', 'xlsx'}


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/upload", methods=["POST"])
def upload():
    if request.method=='POST':
        if 'file' not in request.files:
                flash('No file part')
                print(request.url)
                print("lala")
                return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            temp_dir = TemporaryDirectory(prefix = "upload", suffix="")
            app.config['UPLOAD_FOLDER'] = temp_dir.name
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return results(path)
    return ""

def results(path):
    print(path)
    results = []
    any_errors = False
    if path.endswith("csv"):
        results, any_errors = parse_csv_tsv(path, delimiter=',')
    elif path.endswith("tsv"):
        results, any_errors = parse_csv_tsv(path, delimiter='\t')
    else:
        results, any_errors = parse_excel_file(path)
    temp_obj = NamedTemporaryFile(mode="w",prefix = "results", suffix=".csv", dir = app.config["UPLOAD_FOLDER"], delete=False)
    generate_messages_txt(messages = results, file_obj = temp_obj)
    return send_file(temp_obj.name)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
