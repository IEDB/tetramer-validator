var substrMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        matches.push(str);
      }
    });

    cb(matches);
  };
};

var PTM_names = ["deamidated residue", "dehydrated residue", "formylated residue", "galactosylated residue", "glucosylated residue", "glycosylated residue"];

$('#PTM_display .form-control').typeahead({
  hint: true,
  highlight: true,
  minLength: 1, autoselect: true,
}, {
  name: 'PTM_names',
  source: substrMatcher(PTM_names)
});
