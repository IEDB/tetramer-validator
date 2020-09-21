$(document).ready(function(){

  var engine = new Bloodhound({
  local: ["deamidated residue", "dehydrated residue", "formylated residue", "galactosylated residue", "glucosylated residue", "glycosylated residue"],
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace
});

engine.initialize();

$('#tokenfield-typeahead').tokenfield({
  typeahead: [null, { source: engine.ttAdapter() }]
});

});
