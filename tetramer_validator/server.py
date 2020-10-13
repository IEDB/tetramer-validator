from flask import Flask
from flask import render_template, request, send_from_directory
from tetramer_validator import validate

app = Flask(__name__)

@app.route("/")
def start():
    return render_template(
        "base.html",
    )

@app.route("/output", methods=["POST"])
def output():
    if request.method == "POST":
        input = request.form.to_dict(flat=True)
        print(input)
        num_multimers = len(input["mhc_name"])
        errors = {}
        success = {}
        if num_multimers > 1:
            for multimer in range(num_multimers):
                print(multimer)
                errors[multimer] = validate.validate(
                    pep_seq=input["pep_seq"][multimer], mod_pos=input["mod_pos"][multimer], mod_type=input["mod_type"][multimer], mhc_name=input["mhc_name"][multimer]
                )

                success[multimer] = not errors[multimer]
            render_template("base.html", errors = errors, success=success)
        else:
            errors = validate.validate(pep_seq=input["pep_seq"], mod_pos=input["mod_pos"], mod_type=input["mod_type"], mhc_name=input["mhc_name"])
            success = False
            return render_template(
                "base.html", errors=errors, success=success
            )


@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")


@app.route("/data/<path:filename>")
def send_js(filename):
    return send_from_directory("data", filename=filename)
