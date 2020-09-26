from flask import Flask
from flask import render_template, request, send_from_directory
from tetramer_validator import validate

app = Flask(__name__)


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
        success = False
        if not errors:
            success=True
        return render_template(
            "base.html",
            pep_seq=pep_seq,
            mod_pos=mod_pos,
            mod_type=mod_type,
            mhc_name=mhc_name,
            errors=errors,
            PTM_display=validate.PTM_display,
            success = success
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
            success = False
        )


@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")


@app.route("/data/<path:filename>")
def send_js(filename):
    return send_from_directory("data", filename=filename)
