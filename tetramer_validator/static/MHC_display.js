var MHC_engine = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: {
    url: '/data/molecule.json',
    transform: function(response) {response.data}
  }
});


MHC_engine.initialize();


var substringMatcher = function(strs) {

  return function findMatches(q, cb) {
    var matches, substringRegex;

    //an array that will be populated with substring matches
    matches = [];

    //regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    //terate through the pool of strings and for any string that
    //contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substringRegex.test(str)) {
        matches.push(str);
      }
    });

    cb(matches);
  };
};

$('#MHC_display .form-control').typeahead({
  hint: true,
  highlight: true,
  minLength: 1,
  displayKey: function(obj) {
    obj.Label
  }
}, {
  name: 'MHC-display',
  source: MHC_engine.ttAdapter()
});
