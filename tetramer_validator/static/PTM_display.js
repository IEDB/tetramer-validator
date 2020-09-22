
//var PTM_names1 = new Bloodhound({
  //datumTokenizer: Bloodhound.tokenizers.obj.whitespace('display_name', 'synonyms'),
  //queryTokenizer: Bloodhound.tokenizers.whitespace,
  // url points to a json file that contains an array of country names, see
  // https://github.com/twitter/typeahead.js/blob/gh-pages/data/countries.json
  //prefetch: {
    //url: 'PTM_list.json',
    //cache: false,
    //transform: function(response) { return response.data}
  //},
  //sorter: function(a, b) {
    //return a.score - b.score;
  //},
  //remote: {
    //url: 'query/genes/%QUERY/',
    //wildcard: '%QUERY',
    //transform: function(response) {
      //  return response.data.sort( function(a, b) {
        //    return a.score - b.score;
        //})
    //}
  //}
//});
$(document).ready( function() {
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

$('#PTM_display .form-control').typeahead({
  hint: true,
  highlight: true,
  minLength: 1, autoselect: true,
}, {
  name: 'PTM_names',
  source: substrMatcher(PTM_display)
});
});
