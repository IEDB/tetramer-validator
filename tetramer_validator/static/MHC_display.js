var MHC_engine = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace([
    "Label", "IEDB Label", "synonyms"
  ]),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: {
    url: "/data/molecule.json",
    filter: function(response) {
      return response.data;
    },
    cache: true
  }
});

// initialize the bloodhound suggestion engine
MHC_engine.initialize();

// instantiate the typeahead UI
$('#MHC_display .form-control').typeahead({

  hint: true,
  highlight: true,
  minLength: 1,
  autoselect: true,
}, {
  name: 'MHC_name',
  displayKey: function(mhc) {
    return mhc["IEDB Label"]
  },
  limit: 10,
  source: MHC_engine.ttAdapter()
});
