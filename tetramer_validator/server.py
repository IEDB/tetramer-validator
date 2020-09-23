from flask import Flask
from flask import render_template, request
from tetramer_validator import validate

app = Flask(__name__)


@app.route("/", methods=["GET"])
def output():
    if request.args:
        pep_seq = request.args["pep_seq"]
        mod_pos = request.args["mod_pos"]
        mod_type = request.args["mod_type"]
        mhc_name = request.args["mhc_name"]
        statement = validate.validate(
            pep_seq=pep_seq, mod_pos=mod_pos, mod_type=mod_type, mhc_name=mhc_name
        )
        if not statement:
            statement = "Success! This input is valid"
        return render_template(
            "base.html",
            pep_seq=pep_seq,
            mod_pos=mod_pos,
            mod_type=mod_type,
            mhc_name=mhc_name,
            statement=statement,
            PTM_display=validate.PTM_display,
        )
    else:
        return render_template(
            "base.html",
            pep_seq="",
            mod_pos="",
            mod_type="",
            mhc_name="",
            statement="",
            PTM_display=validate.PTM_display,
        )


@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")
