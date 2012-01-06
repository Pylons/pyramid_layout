
module('popper-example', {

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

    $('#the-node').example({
    });

    $('#the-node').example('destroy');

});


test("Changes label", function() {

    $('#the-node').example({
    });
    equals($('#the-node').text(), 'Hello World!');

    $('#the-node').example('destroy');
    equals($('#the-node').text(), 'The Node Text');

});


test("Label option", function() {

    $('#the-node').example({
        label: 'Bottlecap is awesome!'
    });
    equals($('#the-node').text(), 'Bottlecap is awesome!');

    $('#the-node').example('destroy');
    equals($('#the-node').text(), 'The Node Text');

});

