from flask import Flask
from flask import render_template, request, send_from_directory, redirect, url_for, send_file
from tetramer_validator import validate
from openpyxl import Workbook, load_workbook
from tempfile import NamedTemporaryFile
from tetramer_validator.parse_tables import generate_formatted_data

app = Flask(__name__)


@app.route("/")
def start():
    return render_template("base.html", input=[], list=False)


@app.route("/output", methods=["POST"])
def output():
    if request.method == "POST":
        input = request.form.to_dict(flat=False)
        errors = {}
        print(input)
        if isinstance(input["mhc_name"], list):
            num_multimers = len(input["mhc_name"])
            for multimer in range(num_multimers):
                errors[multimer] = validate.validate(
                    pep_seq=input["pep_seq"][multimer],
                    mod_pos=input["mod_pos"][multimer],
                    mod_type=input["mod_type"][multimer],
                    mhc_name=input["mhc_name"][multimer],
                )
            filename = generate_file(input, errors)
            return render_template("base.html", errors=errors, input=input, list=True, )
    else:
        return redirect(url_for("start"))

def generate_file(input, errors):
     with NamedTemporaryFile(prefix="your_input_",suffix=".xlsx",dir="static", delete=False) as input_obj:
        input_data = Workbook()
        ws = input_data.active
        ws.append(('MHC Molecule', 'Peptide Sequence', 'Modification Position', 'Modification Type'))
        for row in zip(*(input.values())):
            ws.append(row)
        input_data.save(input_obj.name)
        header_dict = {'mhc_name': 'A', 'pep_seq': 'B', 'mod_pos': "C", 'mod_type': "D"}
        for input_num in errors.keys():
            errorlist = errors[input_num]
            list(map(lambda error: error.update({"cell": header_dict[error["field"]] + str(input_num + 1)}), errorlist))
        print(errors)
        generate_formatted_data(input_obj.name, errors)

@app.route("/README.html", methods=["GET"])
def readme():
    return render_template("README.html")


@app.route("/data/<path:filename>")
def send_data(filename):
    return send_from_directory("data", filename=filename)

@app.route("/downloads/<path:filename>")
def download_input(filename):
    return send_file('static', filename=filename)
