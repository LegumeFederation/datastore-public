define(['datastore', 'backbone', 'jquery', 'utils', 'shCore'], function(Datastore, Backbone, $, Utils, SyntaxHighlighter) {
    console.log(SyntaxHighlighter);
    var Highlighter = {
        Views: {},
        BrushSources: {}
    };

    Utils.load_css('static/syntaxhighlighter/styles/shCore.css');
    Utils.load_css('static/syntaxhighlighter/styles/shThemeDefault.css');

    Highlighter.BrushSources = {
        'php': 'shBrushPhp',
        'js': 'shBrushJScript',
        'css': 'shBrushCss',
        'py': 'shBrushPython',
        'fasta': 'shBrushFasta'
    };

    Highlighter.Views.MainView = Backbone.View.extend({
        initialize: function(options) {
            console.log(this.model);
            console.log(options);
            if (!this.options.brush)
                this.options.brush = 'text';

            var ext = this.model.get('path').split('.').pop();
            this.brush_source = Highlighter.BrushSources[ext] || 'shBrushPlain';
            console.log(this.brush_source);
        },
        render: function() {
            console.log(this.options.brush);
            var self = this;
            $.get('serve' + this.model.get('path'), function(data, text_status, jqXHR) {
                var $pre = $("<pre>", {'class' : 'brush: ' + self.options.brush}).append(_.escape(data));
                require([self.brush_source], function(brush) {
                    SyntaxHighlighter.highlight($pre);
                    $pre.appendTo(self.$el);
                });
            });
            return this;
        }
    });

    return Highlighter;
});
