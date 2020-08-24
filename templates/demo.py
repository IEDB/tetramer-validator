from flask import Flask
from flask import render_template, request, redirect, url_for
from . import validate

app = Flask(__name__)


@app.route("/")
def start():
    return render_template("test.html")


@app.route("/output", methods=["POST"])
def output():
    if request.method == "POST":
        pep_seq=request.form["pep_seq"]
        mod_pos=request.form["mod_pos"]
        mod_type=request.form["mod_type"]
        mhc_name=request.form["mhc_name"]
        statement = validate.validate(pep_seq = pep_seq, mod_pos= mod_pos, mod_type = mod_type, mhc_name = mhc_name)
        return render_template(
            "test1.html", pep_seq = pep_seq, mod_pos= mod_pos, mod_type = mod_type, mhc_name = mhc_name, statement = statement
        )
