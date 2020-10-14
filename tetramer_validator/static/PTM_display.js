var PTM_names = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.ngram(["value", "IEDB_synonym_1", "IEDB_synonym_2", "synonym_1", "synonym_2"]),
  queryTokenizer: Bloodhound.tokenizers.ngram,
  prefetch: {
    url: "/data/PTM_list.json",
    filter: function(response) {
      return response.data;
    },
    cache: true,
    thumbprint: true
  },
  matchAnyQueryToken: true
});

// initialize the bloodhound suggestion engine
PTM_names.initialize();

// multiselect
$('#mod_type').tokenfield({
  typeahead: [{
    hint: true,
    highlight: true,
    minLength: 1,
    autoselect: true,
  }, {
    name: 'PTM_names',
    displayKey: function(ptm) {
      return ptm.value;
    },
    source: PTM_names.ttAdapter(),
    templates: {
        suggestion: function (ptm) {
          var names = [];
          names.push(ptm.value);
          if(ptm.IEDB_synonym_1 != null) {
            names.push(ptm.IEDB_synonym_1);
          }
          if(ptm.IEDB_synonym_2 != null) {
            names.push(ptm.IEDB_synonym_2);
          }
          if(ptm.synonym_1 != null) {
            names.push(ptm.synonym_1);
          }
          if(ptm.synonym_2 != null) {
            names.push(ptm.synonym_2);
          }
          //names.push("</p>")
          return_html = '<p>' + names.join(" - ") + '</p>';
          return return_html;
        }
      },
    limit: 10
  }]
});
