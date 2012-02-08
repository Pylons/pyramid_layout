/*jslint undef: true, newcap: true, nomen: false, white: true, regexp: true */
/*jslint plusplus: false, bitwise: true, maxerr: 50, maxlen: 80, indent: 4 */
/*jslint sub: true */

/*globals window navigator document console setTimeout $ */

(function ($) {

    "use strict";

    var log = function () {
        if (window.console && console.log) {
            // log for FireBug or WebKit console
            console.log(Array.prototype.slice.call(arguments));
        }
    };

    $.widget('popper.tagbox', {

        options: {
            // set intial data source
            initialDataSource: null,
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

        _create: function () {
            var self = this,
                el = this.element,
                o = this.options;

            this.initialDataSource = o.initialDataSource ?
                o.initialDataSource : this._initialDataSource;
            this.displayError = o.displayError ?
                o.displayError : this._displayError;
            this.ajaxError = o.ajaxError ? o.ajaxError : this._ajaxError;
            this.addTag = o.addTag ? o.addTag : this._addTag;
            this.deleteTag = o.deleteTag ? o.deleteTag : this._deleteTag;
            //this.ajaxManager = $.manageAjax.create(
            //    'tagbox',
            //    {queue: true, cacheResponse: true}
            //);
            el.addClass('tags');
            var tagbox_data = this.initialDataSource();
            el.append(this._renderTags(tagbox_data));
            el.append(this._renderForm());

            this.tagList = el.children('ul');
            this.addTagForm = el.children('form.addTag').first();
            this.addTagForm.bind('submit', this._addTag);
        },

        destroy: function () {
            this.element.text(this.oldText);
            $.Widget.prototype.destroy.call(this);
        },

        _setOption: function (key, value) {
            console.log('Set Option');
        },

        _initialDataSource: function () {
            return window.head_data.tagbox;
        },

        _displayError: function () {
            console.log('Display Error');
        },

        _ajaxError: function () {
            console.log('Ajax Error');
        },

        _renderForm: function () {
            var form = '<form action="#" class="addTag">' +
                '<fieldset>' +
                '<input id="newTag" type="text" name="tag"' +
                ' placeholder="A tag to add" />' +
                '<button type="submit">New Tag</button>' +
                '</fieldset>' +
                '</form>';
            return form;
        },

        _renderTag: function (item, docid) {
            var personal = (item.snippet !== 'nondeleteable') ? 'personal' : '';
            var li = '<li><a href="/pg/showtag/' + item.tag + '" class="tag ' +
                personal + '">' + item.tag + '</a>';
            if (personal) {
                li += '<a title="Remove Tag" href="#" class="removeTag">x</a>';
            }
            li += '<a href="/pg/taguser.html?tag=' + item.tag + '&docid=' +
                docid + '" class="tagCounter">' + item.count + '</a>';
            return li;
        },

        _renderTags: function (data) {
            var self = this;
            var ul = $('<ul></ul>');
            $.each(data.records, function (idx, item) {
                var li = self._renderTag(item, data.docid);
                ul.append(li);
            });
            return ul;
        },

        _addTag: function (event) {
            var tagList = $(this).prev('ul').first();
            var newTag = $(this).find('#newTag').first().val();
            if (newTag) {
                tagList.append('<li><a href="/pg/showtag/' + newTag +
                    '" class="tag personal">' + newTag + '</a>' +
                    '<a title="Remove Tag" href="#" class="removeTag">x</a>' +
                    '<a href="/pg/taguser.html?tag=' + newTag +
                    '" class="tagCounter">1</a></li>');
            }
            return false;
        },

        _deleteTag: function () {
            console.log('Delete Tag');
        }

    });

})(window.jQuery);
