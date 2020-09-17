from flask import Flask
from flask import render_template, request
import validate

app = Flask(__name__)


@app.route("/", methods=["GET"])
def output():
    if request.args:
        pep_seq = request.args["pep_seq"]
        mod_pos = request.args["mod_pos"]
        mod_type = requests.args["mod_type"]
        mhc_name = request.args["mhc_name"]
        statement = validate.validate(
            pep_seq=pep_seq, mod_pos=mod_pos, mod_type=mod_type, mhc_name=mhc_name
        )
        if not statement:
            statement = "Success! This input is valid"
        return render_template(
            "test1.html",
            pep_seq=pep_seq,
            mod_pos=mod_pos,
            mod_type=mod_type,
            mhc_name=mhc_name,
            statement=statement,
        )
    else:
        return render_template(
            "test1.html", pep_seq="", mod_pos="", mod_type="", mhc_name="", statement=""
        )
