
module('popper-tagbox', {

    setup: function() {
        var self = this;
        $('#main').append(
            '<div id="the-node">The Node Text</div>'
        );
    },

    teardown: function() {
        $('#main').empty();
    }

});


test("Create / destroy", function() {

    $('#the-node').tagbox({
    });

    $('#the-node').tagbox('destroy');

});


test("Changes label", function() {

    $('#the-node').tagbox({
    });
    equals($('#the-node').text(), 'Popper TagBox!');

    $('#the-node').tagbox('destroy');
    equals($('#the-node').text(), 'The Node Text');

});


test("Label option", function() {

    $('#the-node').tagbox({
        label: 'Bottlecap is awesome!'
    });
    equals($('#the-node').text(), 'Bottlecap is awesome!');

    $('#the-node').tagbox('destroy');
    equals($('#the-node').text(), 'The Node Text');

});

