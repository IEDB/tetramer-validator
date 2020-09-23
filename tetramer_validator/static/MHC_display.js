$(document).ready(function () {

var MHC_names = new Bloodhound({
datumTokenizer: Bloodhound.tokenizers.obj.whitespace('Label', 'IEDB Label', 'synonyms'),
queryTokenizer: Bloodhound.tokenizers.whitespace,
 //url points to a json file that contains an array of country names
prefetch: {
url: '/data/molecule.json',
cache: true,
transform: function(response) { return response.Label}
}
}
$('#MHC_names .typeahead').typeahead({
  hint: true,
  highlight: true,
  minLength: 1
},
{
  name: 'states',
  source: MHC_names
});
)
