from flask import Flask
from flask import render_template, request, send_from_directory, redirect
from tetramer_validator import validate

app = Flask(__name__)

@app.route("/")
def start():
    return render_template(
        "base.html", input=[], list=False
    )

@app.route("/output", methods=["POST"])
def output():
    if request.method == "POST":
        input = request.form.to_dict(flat=False)
        errors = {}
        if isinstance(input["mhc_name"], list):
            num_multimers = len(input["mhc_name"])
            for multimer in range(num_multimers):
                errors[multimer] = validate.validate(
                    pep_seq=input["pep_seq"][multimer], mod_pos=input["mod_pos"][multimer], mod_type=input["mod_type"][multimer], mhc_name=input["mhc_name"][multimer]
                )
            return render_template("base.html", errors = errors, input=input, list=True)
    else:
        return redirect(url_for('start'))

@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")


@app.route("/data/<path:filename>")
def send_js(filename):
    return send_from_directory("data", filename=filename)

@app.route("/")
