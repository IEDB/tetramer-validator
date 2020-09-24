# Documentation

## Instructions for Web form

Please enter a peptide sequence, modification type, modification position, and/or the name of MHC molecule.

Each modification position should be of the format `<amino acid><position>`

Modification type should be chosen from autocomplete list.  If not chosen from the autocomplete list, validation will not be successful.

MHC molecule name should be chosen from autocomplete list. If not chosen from the autocomplete list, validation will not be successful.

Either modification position **and** modification type must be provided or no modification information should be entered.

NULL is not an appropriate value for any field. Please leave empty if there is no appropriate value.

## Example of Valid Entry

See below for an example for the following entry.

Peptide Sequence: NLVPMVATV

Modification Type: Oxidation

Modification Position: M5

MHC Name: HLA-A*02:01

![1]
[1]: tetramer_validator/static/Example_1

Notice that there is the display name of oxidized residue for Oxidation. Please choose from the display names or else validation will not be successful.  

Also, notice that syntax of M5. The modification is at the position 5 and the amino acid is methionine.  
