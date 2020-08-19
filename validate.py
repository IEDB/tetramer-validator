import csv

path = "molecule.tsv"
with open(path) as fh:
    reader = csv.DictReader(fh, delimiter="\t")
    molecules = [
        molecule["IEDB Label"]
        for molecule in reader
        if molecule["Restriction Level"] == "complete molecule"
        or molecule["Restriction Level"] == "partial molecule"
    ]

def validate(pep_seq, mhc_name, mod_type=None, mod_pos=None):
    if mod_pos:
        statement = mod_pos_val(pep_seq, mod_pos)
        if statement is 0:
            return 0
    if mhc_name:
        statement = pep_seq_mhc_name_val(pep_seq, mhc_name)
        if statement is 0:
          return 0
    return None

def validate_pep_seq_mhc_name(pep_seq, mhc_name):
   if mhc_name not in molecules:
      print(f"{mhc_name} is not a valid MHC name")
      return 0
   return None
   #Need to know how to match mhc_name with pep_seq
   #elif mhc_name:
   #else:
     # return None

def validate_mod_pos(pep_seq, mod_pos):
    split = mod_pos.split(",")
    modifications = [(mod[0], int(mod[1])) for mod in split]
    pep_seq_tuple = [(peptide, index) for index, peptide in enumerate(pep_seq)]
    
    for mod in modifications:
        if mod not in pep_seq_tuple:
            print(f"This peptide sequence %s does not contain %s at position %d", pep_seq, mod[0], mod[1])
            return 0
    return None

def test_validate_one():
  assert validate(pep_seq = "NLVPMVATV", mhc_name = "HLA-A*02:01", mod_pos = "K4") == 0

def test_validate_two():
  assert validate(pep_seq = "NLVPMVATV", mhc_name = "HLA-A*02:01", mod_pos = "M4") == None

def test_mod_pos_val_one():
    assert mod_pos_val(pep_seq="NLVPMVATV", mod_pos="M4") == None

def test_mod_pos_val_two():
    assert mod_pos_val(pep_seq="NLVPMVATV", mod_pos="K4") == 0

def test_mod_pos_val_three():
    assert mod_pos_val(pep_seq="NLVPOVATV", mod_pos="M4") == 0