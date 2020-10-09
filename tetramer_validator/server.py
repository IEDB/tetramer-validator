from flask import Flask
from flask import render_template, request, send_from_directory
from tetramer_validator import validate

app = Flask(__name__)

@app.route("/")
def start():
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

@app.route("/output", methods=["POST"])
def output():
    if request.method == "POST":
        pep_seq = request.form["pep_seq"]
        mod_pos = request.form["mod_pos"]
        mod_type = request.form["mod_type"]
        mhc_name = request.form["mhc_name"]
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


@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")


@app.route("/data/<path:filename>")
def send_js(filename):
    return send_from_directory("data", filename=filename)
