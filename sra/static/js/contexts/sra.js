define(['datastore', 'backbone', 'jquery', 'utils'], function(Datastore, Backbone, $, Utils) {
    var SRA = {
        Collections: {},
        Models: {},
        Views: {},
        Events: {},
    };

    SRA.Models.Study = Backbone.Model.extend({
        url: function() {
            return '/api/file?path=' + this.get('path');
        },
        parse: function(data) {
            metadata = Utils.metadata_to_object(data.metadata);
            return {
                id: data.name,
                path: data.path,
                'abstract': metadata['abstract'],
                title: metadata['title'],
                description: metadata['description']
            };
        }
    });

    SRA.Collections.StudyCollection = Backbone.Collection.extend({
        model: SRA.Models.Study
    });

    SRA.Views.StudyList = Backbone.View.extend({
        tagName: 'div',
        id: 'sra-sidebar',
        className: 'span4',
        events: {
            'click li a': 'select_study'
        },
        initialize: function(options) {
            console.log(options);
            this.collection.bind('reset', this.add_studies, this);
            this.collection.bind('select', this.highlight_study, this);
        },
        render: function() {
            return this;
        },
        add_studies: function() {
            this.$el.empty();
            var $list = $('<ul>', {id: 'study-list'});
            console.log(this.collection);
            this.collection.each(function(model) {
                new SRA.Views.StudyListItem({model: model}).render().$el.appendTo($list);
                model.fetch();
            });
            this.$el.append($list);
        },
        select_study: function(e) {
            var model = $(e.currentTarget).closest('li').data('model');
            console.log(model);
            this.collection.trigger('select', model);
        },
        highlight_study: function(model) {
            var $children = this.$el.find('ul').children().removeClass('active');
            if (model)
                $children.filter('li[data-model_id="' + model.id + '"]').addClass('active');
        }
    });

    SRA.Views.StudyListItem = Backbone.View.extend({
        tagName: 'li',
        initialize: function() {
            this.model.bind('sync', this.render, this);
        },
        render: function() {
            this.$el
                .empty()
                .append(
                    $('<a>', {href: '#'/*'#study/' + model.id*/})
                        .append($('<span>', {'class': 'study-id'}).append(this.model.id))
                        .append($('<span>', {'class': 'study-title'}).append(this.model.get('title') || '&nbsp;'))
                )
                .data('model', this.model)
                .attr('data-model_id', this.model.id);
            return this;
        }
    });

    SRA.Views.ContentArea = Backbone.View.extend({
        id: 'sra-content',
        className: 'span8',
        initialize: function(options) {
            var self = this;
            /*
            $('#header a').click(function(e) {
                e.preventDefault();
                this.collection.trigger('select', null);
                App.router.navigate('');
                return false;
            });
            */
            this.collection.bind('select', this.display_study, this);
        },
        render: function() {
            this.$el
                .empty()
                .append($('<h2>').append('Welcome to the iPlant Sequence Database!'))
                .append($('<p>').append('Click on a study to the left to explore details and download sequence reads.'));
            return this;
        },
        display_study: function(study) {
            if (!study) {
                this.render();
                return;
            }
            this.$el.empty();

            $('<h2>')
                .append(study.id + ' ' + study.get('title'))
                .appendTo(this.$el);

            var $dl = $('<dl>')
                .append($("<dt>").append("Abstract"))
                .append($("<dd>").append(study.get('abstract')));

            var desc;
            if ((desc = study.get('description')) != null)
                $dl.append($("<dt>").append("Description"))
                .append($("<dd>").append(desc));

            $dl.appendTo(this.$el);

            $('<h3>').append('Reads').appendTo(this.$el);

            $('<div>', {'class': 'file-tree'}).appendTo(this.$el).fileTree({
                root: study.get('path'),
                script: '/api/ls'
            }, function(file) {
                console.log(file); 
                window.location.replace('/download?path=' + encodeURIComponent(file));
            });

        }
    });

    SRA.Views.MainView = Backbone.View.extend({
        tagName: 'div',    
        initialize: function() {
            console.log(this.model);
            console.log(this.collection);
        },
        render: function() {
            var $container = $('<div>', {'class': 'row'});
            var study_collection = new SRA.Collections.StudyCollection();
            var study_list = new SRA.Views.StudyList({
                collection: study_collection
            }).render();
            var content_area = new SRA.Views.ContentArea({
                collection: study_collection
            }).render();
            $container
                .append(study_list.el)
                .append(content_area.el)
                .appendTo(this.$el);

            var self = this;
            this.collection.bind('reset', function() {
                var models = _.map(self.collection.models, function(model) {
                    return new SRA.Models.Study({
                        id: model.get('name'),
                        path: model.get('path')
                    });
                });
                study_collection.reset(models);
            });
            return this;
        }
    });
    return SRA;
});
