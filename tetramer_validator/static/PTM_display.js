var PTM_names = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace(["value", "IEDB_synonym_1", "IEDB_synonym_2", "synonym_1", "synonym_2"]),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: {
    url: "/data/PTM_list.json",
    filter: function(response) {
      return response.data;
    }
  }
});

// initialize the bloodhound suggestion engine
PTM_names.initialize();

$('#PTM_display_1').tokenfield({
  typeahead: [{
    hint: true,
    highlight: true,
    minLength: 1,
    autoselect: true,
  }, {
    name: 'PTM_names',
    displayKey: function(ptm) {
      return ptm.value
    },
    source: PTM_names.ttAdapter()
  }]
});
