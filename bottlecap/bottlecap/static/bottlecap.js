
/* Gumball javascript */

(function($) {

var log = function() {
    if (window.console && console.log) {
        // log for FireBug or WebKit console
        console.log(Array.prototype.slice.call(arguments));
    }
};

/* QuickPanel */

$.widget('gumball.quickpanel', {

    options: {
        width: 600
    },

    _create: function() {
        var self = this;
        this.hasOpenedOnce = false;

        // Figure out the quickpanel identifiers.
        var originalText = this.element.find('a').text()
        var panelId = 'quickpanel-' + originalText.toLowerCase();
        var panelTitle = originalText + " Quickpanel";

        // Find the panel.
        this.panel = $('#' + panelId);

        // The quickpanel is not defined, so nothing to do.
        if (this.panel.length == 0) {
            return;
        }

        // Find the positioning element.
        this.positionElement = this.element.find('.local-nav-link, .members-local-nav-link');
        if (this.positionElement.length == 0) {
            // members nav has no local nav link
            this.positionElement = this.element;
        }

        this._position = {
            my: 'left top',
            at: 'left bottom',
            offset: '-64 0',
            of: this.positionElement,
            collision: 'fit none'
        };

        // Bind the dialog.
        this.panel.dialog({
            autoOpen: false,
            dialogClass: 'quickpanel-dialog',
            title: panelTitle,
            width: this.options.width,
            position: this._position,
            drag: function(evt) {
                self.northTail.hide();
            },
            close: function(evt) {
                self.northTail.hide();
                self.southTail.hide();
                $('body').data('quickpanel-opened', null);
            }
        });

        // Bind the dialog opening.
        this.positionElement.mouseenter(function(evt) {
            self.southTail
                .show()
                .position({
                    my: 'left center',
                    at: 'right center',
                    of: self.positionElement,
                    offset: '2 -3',
                    collision: 'none none'
                })
                .data('quickpanel-assigned', self.element);
        });
        $('body').mouseover(function(evt) {
            if (! $(evt.target).is('#local, #local *, .quickpanel-south-tail')) {
                self.southTail.hide('fast');
            }
        });

        // add the north tail
        this.northTail = $('.quickpanel-north-tail');
        if (this.northTail.length === 0) {
            this.northTail = $('<div></div>')
                .addClass('quickpanel-north-tail north-tail')
                .hide()
                .appendTo('body');
        }
        // add the south tail
        this.southTail = $('.quickpanel-south-tail');
        if (this.southTail.length === 0) {
            this.southTail = $('<div></div>')
                .addClass('quickpanel-south-tail south-tail')
                .hide()
                .click(function(evt) {
                    var southTailAssignment = $(this).data('quickpanel-assigned');
                    southTailAssignment.quickpanel('open', evt);
                    self.southTail.hide('fast');
                })
                .appendTo('body');
        }


    },

    destroy: function() {
        this.panel.dialog('destroy');
        $.Widget.prototype.destroy.call( this );
    },

    open: function(evt) {
        // We allow only one dialog open in the document
        var openedPanel = $('body').data('quickpanel-opened');
        if (openedPanel) {
            openedPanel.quickpanel('close');
        }
        $('body').data('quickpanel-opened', this.element);
        // open the dialog
        this.panel.dialog('open');
        // re-position the dialog on subsequent opens
        this.reposition();
        // show the north tail
        this.northTail
            .show()
            .position({
                my: 'center bottom',
                at: 'center bottom',
                of: this.positionElement,
                collision: 'none none'
            });

    },

    close: function(evt) {
        this.panel.dialog('close');
    },

    reposition: function() {
        if (! this.hasOpenedOnce) {
            this.hasOpenedOnce = true;
        } else {
            // re-setting its position will reposition the dialog
            this.panel.dialog('option', 'position', this._position);
        }
        // Extra positioning. The panel shall fit into #content.
        // (This is something jquery-ui positioning does not do for us.)
        var panelWidget = this.panel.dialog('widget');
        var content = $('#content');
        var contentLeft = content.position().left;
        var contentRight = contentLeft + content.outerWidth();
        var panelLeft = panelWidget.position().left;
        var panelRight = panelLeft + panelWidget.outerWidth();
        if (panelRight > contentRight) {
            var newLeft = (panelLeft - panelRight + contentRight);
            if (newLeft >= contentLeft) {
                panelWidget.css('left', '' + newLeft + 'px');
            }
        }
    }

});


})(jQuery);
