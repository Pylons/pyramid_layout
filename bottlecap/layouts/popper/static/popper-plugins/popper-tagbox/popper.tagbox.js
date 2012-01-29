(function($) {

var log = function() {
    if (window.console && console.log) {
        // log for FireBug or WebKit console
        console.log(Array.prototype.slice.call(arguments));
    }
};

$.widget('popper.tagbox', {

    options: {
        // display an error to the user if validation fails
        displayError: null,
        // called when there is an ajax error
        ajaxError: null,
        // function to call to render items from ajax request
        renderTags: null,
        // called when an item is added from the list
        addTag: null,
        // called when an item is deleted from the list
        deleteTag: null
    },

    _create: function() {
        var self = this;
        var el = this.element;
        var o = this.options;

        this.displayError = o.displayError ? o.displayError : this._displayError;
        this.ajaxError = o.ajaxError ? o.ajaxError : this._ajaxError;
        this.addTag = o.addTag ? o.addTag : this._addTag;
        this.deleteTag = o.deleteTag ? o.deleteTag : this._deleteTag;
        //this.ajaxManager = $.manageAjax.create(
        //    'tagbox',
        //    {queue: true, cacheResponse: true}
        //);
        el.addClass('tags');
        console.log('TAGS')
        console.log(el)
        var tagbox_data = window.head_data.tagbox_data;
        el.append(this._renderTags(tagbox_data));
        el.append(this._renderForm());

        this.tagList = el.children('ul');
        this.addTagForm = el.children('form.addTag').first();
        this.addTagForm.bind('submit', this._addTag);
    },

    destroy: function() {
        this.element.text(this.oldText);
        $.Widget.prototype.destroy.call(this);
    },

    _setOption: function(key, value) {
        console.log('Set Option');
    },

    _displayError: function() {
        console.log('Display Error');
    },

    _ajaxError: function() {
        console.log('Ajax Error');
    },

    _renderForm: function() {
        form = '<form action="#" class="addTag">' +
               '<fieldset>' +
               '<input id="newTag" type="text" name="tag" placeholder="A tag to add" />' +
               '<button type="submit">New Tag</button>' +
               '</fieldset>' +
               '</form>' 
        return form; 
    },

    _renderTag: function(item) {
        li = '<li><a href="'+item.tag.href+'" class="'+item.tag.class+'">'+
             item.tag.name+'</a>';
        if (item.remove) {
            li += '<a title="'+item.remove.title+'" href="'+item.remove.href+
                  '" class="removeTag">x</a>';
        }
        li += '<a href="'+item.counter.href+'" class="tagCounter">'+
              item.counter.value+'</a>';
        return li
    },

    _renderTags: function(data) {
        var self = this
        var ul = $('<ul></ul>');
        $.each(data.items, function(idx, item) {
            li = self._renderTag(item);
            ul.append(li);    
        })
        return ul;
    },

    _addTag: function(event) {
        var tagList = $(this).prev('ul').first();
        var newTag = $(this).find('#newTag').first().val();
        if (newTag) {
            tagList.append('<li><a href="#tag" class="tag personal">' + 
                newTag + '</a>' +
                '<a title="Remove Tag" href="#" class="removeTag">x</a>' +
                '<a href="#ppl" class="tagCounter">1</a></li>');
        }
        return false;
    },

    _deleteTag: function() {
        console.log('Delete Tag');
    }

});


})(jQuery);
