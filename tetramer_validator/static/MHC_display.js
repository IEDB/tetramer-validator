
//var MHC_engine = new Bloodhound({
//  datumTokenizer: Bloodhound.tokenizers.obj.whitespace("Label", "IEDB Label", "synonyms"),
  //queryTokenizer: Bloodhound.tokenizers.whitespace,
  //local: [{
  //"Label": "Po",
  //  "IEDB Label": "Poa",
  //"synonyms": "Poal"
  //}],
//  identify: function(obj) {
//    obj.Label;
//  },
//  prefetch: {
//    url: '/data/molecule.json',
//    transform: function(request) {
//      request.data
//    }
//  }
//});




$(document).ready(


  function() {
    var MHC_names;
    $.getJSON("/data/molecule.json", function(json) { MHC_names = json; console.log(MHC_names); });

    var substringMatcher = function(strs) {
      return function findMatches(q, cb) {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
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
      source: substringMatcher(MHC_names)
    });
  });
