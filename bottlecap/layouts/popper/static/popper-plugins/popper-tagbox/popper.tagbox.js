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
            prevals: null,
            validateRegexp: null,
            docid: null,
            showtag_url: null,
            tagusers_url: null,
            name: null,
            searchTagURL: null,
            addTagURL: null,
            delTagURL: null
        },

        _create: function () {
            var self = this,
                el = this.element,
                o = this.options;

            this.prevals = o.prevals ? o.prevals : this._getPrevals();
            el.addClass('tagbox');
            var tagbox_data = this.prevals;
            el.append(this._renderTags(tagbox_data));
            el.append(this._renderForm());

            this.tagList = el.children('ul');
            this.addTagForm = el.children('form.addTag').first();
            this.addTagForm.bind('submit',
                $.proxy(this._addTag, this));
            $('.removeTag').live('click', 
                $.proxy(this._delTag, this));
        },

        destroy: function () {
            this.addTagForm.unbind('submit',
                $.proxy(this._addTag, this));
            $('.removeTag').unbind('click', 
                $.proxy(this._delTag, this));
        },

        _setOption: function (key, value) {
            console.log('Set Option');
        },

        _getPrevals: function () {
            return window.head_data.panel_data.tagbox;
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
                docid + '" class="tagCounter">' + item.count + '</a>' +
                '<input type="hidden" name="box" value="' +
                item.tag + '"></li>';
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

        _addTag: function (e) {
            e.preventDefault();
            var self = this;
            var tagInput = self.addTagForm.find('#newTag').first();
            var newTag = tagInput.val();
            if (newTag) {
                if (!self._validateTag(newTag)) {
                    return false;
                }
                if (self.options.addTagURL) {
                    $.ajax({
                        url: self.options.addTagURL,
                        data: {'val': newTag},
                        type: 'POST',
                        dataType: 'json',
                        success: function (data, textStatus, xhr) {
                            self._addTagListItem(newTag);
                            self._ajaxSuccess(data, textStatus, xhr);
                        },
                        error: function (xhr, textStatus) {
                            self._ajaxError(xhr, textStatus);
                        }
                    });
                } else {
                    self._addTagListItem(newTag);
                }
            }
            tagInput.val('');
            return false;
        },

        _addTagListItem: function (tag) {
            var self = this;
            self.tagList.append('<li><a href="/pg/showtag/' + tag +
                '" class="tag personal">' + tag + '</a>' +
                '<a title="Remove Tag" href="#" class="removeTag">x</a>' +
                '<a href="/pg/taguser.html?tag=' + tag +
                '" class="tagCounter">1</a>' + 
                '<input type="hidden" name="box" value="' + tag + '"></li>');
            return;
        },

        _validateTag: function (tag) {
            if (this.options.validateRegexp) {
                if (tag.match(this.options.validateRegexp) === null) {
                    log('Value contains characters that ' +
                        'are not allowed in a tag.');
                    return false;
                }
            }
            return true;
        },

        _delTag: function (e) {
            var self = this;
            var target = $(e.target);
            var tag = target.siblings('.tag')[0].innerText || null;
            if (tag) {
                if (self.options.delTagURL) {
                    $.ajax({
                        url: self.options.delTagURL,
                        data: {'val': tag},
                        type: 'POST',
                        dataType: 'json',
                        success: function (data, textStatus, xhr) {
                            self._delTagListItem(target);
                            self._ajaxSuccess(data, textStatus, xhr);
                        },
                        error: function (xhr, textStatus) {
                            self._ajaxError(xhr, textStatus);
                        }
                    });
                } else {
                    self._delTagListItem(target);
                }
            }
        },

        _delTagListItem: function (target) {
            target.closest('li').remove();
        },

        _ajaxSuccess: function (data, textStatus, xhr) {
            log(textStatus);
        },

        _ajaxError: function (xhr, textStatus) {
            log(textStatus);
        }

    });

})(window.jQuery);
