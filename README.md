# Documentation

## General Instructions
1. Please enter MHC molecule and peptide sequence. Both of these fields are required. Optionally, one can enter modification information.
2. MHC molecule name should be chosen to conform to [MHC Restriction ontology](https://www.ebi.ac.uk/ols/ontologies/mro).
3. Modification Position field should be a comma separated list of amino acid letter followed by position number (e.g. F1, S10, S300). Each modification position should be of the format `<amino acid><position>`
4. Modification type should be chosen to conform to [PSI-MOD ontology](https://www.ebi.ac.uk/ols/ontologies/mod).  
5. Either modification position **and** modification type must be provided or no modification information should be entered.
6. There should be equal number of modification positions and modification types.
7. NULL is not an appropriate value for any field. Please leave empty if there is no appropriate value.

## Further Instructions for Web Form
In order to assist user, the MHC Molecule and Modification Type fields output suggestions that conform to MHC Restriction ontology and PSI-MOD ontology, respectively.  Please use the suggested names to ensure successful validation.

## Example of Valid Entry

See below for an example for entering the following entry.

* MHC Molecule: HLA-A*02:01
* Peptide Sequence: NLVPMVATV
* Modification Type: Oxidation
* Modification Position: M5

[TODO: Add screenshot]

* Notice that there is the display name of oxidized residue for Oxidation. Please choose from the display names or else validation will not be successful. 
* Notice that syntax of M5. The modification is at the position 5 and the amino acid is methionine.  
