
module('popper-tagbox', {

    setup: function() {
        var self = this;
        $('#main').append(
            '<div id="the-node"></div>'
        );
        // XXX Instead of falling back on window.head_data, the widget should
        // rely on options. TODO
        window.head_data = {'panel_data': {'tagbox': {
            "records": [
                {"count": 2, "snippet": "nondeleteable", "tag": "flyers"},
                {"count": 2, "snippet": "nondeleteable", "tag": "park"}
            ],
            "docid": -1352878729
        }}};
        
    },

    teardown: function() {
        $('#main').empty();
    }

});


test("Create / destroy", function() {

    $('#the-node').tagbox({
    });

    $('#the-node').tagbox('destroy');

    ok(true);

});


test("autocomplete", function() {

    $('#the-node').tagbox({
        autocompleteURL: 'http://foo.bar/autocomplete.json'
    });

    

    $('#the-node').tagbox('destroy');

    ok(true);

});




