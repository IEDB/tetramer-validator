var countries = new Bloodhound({
  datumTokenizer: function(data) {
      return Bloodhound.tokenizers.whitespace(data.value);
  },
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: "/data/molecule.json",
    filter: function(response) {
      return response.data;
    }
  }
});

// initialize the bloodhound suggestion engine
countries.initialize();

// instantiate the typeahead UI
$('#MHC_display .form-control').typeahead(
  { hint: true,
    highlight: true,
    minLength: 1
  },
  {
  name: 'countries',
  //displayKey: function(countries) {
    //return countries;
  //},
  source: countries.ttAdapter()
});
