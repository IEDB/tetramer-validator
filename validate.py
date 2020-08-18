import csv

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




