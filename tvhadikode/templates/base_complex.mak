<%inherit file="base_simple.mak"/>

<%block name="header">
    <div class="form-group has-feedback" id="input-search-container">
        <input type="text" class="form-control typeahead" placeholder="Programm oder Kanal..." aria-describedby="input-search-status" id="input-search">
        <span class="glyphicon glyphicon-search form-control-feedback" aria-hidden="true"></span>
        <span id="input-search-status" class="sr-only">(Suche)</span>
    </div>
</%block>

<%block name="javascript_src">
    <script src="${request.static_path('tvhadikode:static/js/typeahead.bundle.js')}"></script>
</%block>

<%block name="javascript">
    var serviceProvider = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('service'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '${request.route_path('ajax.search.services')}',
    });

    var programsProvider = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('service'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: '${request.route_path('ajax.search.programs', query='_QUERY_')}',
            wildcard: '_QUERY_'
        }
    });

    // prevents caching
    serviceProvider.clear();
    serviceProvider.clearPrefetchCache();
    serviceProvider.initialize(true);

    var serviceTemplate = function(obj) {
        if (obj.current_program) {
            return '<div class="tt-suggestion tt-item">\
                ' + obj.service + '\
                <span class="text-muted">&mdash; ' + obj.current_program + '</span>\
                </div>';
        } else {
            return '<div class="tt-suggestion tt-item">\
                ' + obj.service + '\
                </div>';
        }
    }

    var programTemplate = function(obj) {
        return '<div class="tt-suggestion tt-item">\
            ' + obj.name + '\
            <span class="text-muted">\
            &mdash; ' + obj.service + '\
            &mdash; ' + obj.start + '</span>\
            </div>';
    }

    $(function() {
        $('#input-search').typeahead({
            highlight: true,
            limit: 8
        }, {
            source: serviceProvider,
            display: 'service',
            templates: {
                suggestion: serviceTemplate,
                header: '<div class="tt-suggestion tt-header">Kanäle</div>'
            }
        }, {
            source: programsProvider,
            display: 'name',
            templates: {
                suggestion: programTemplate,
                header: '<div class="tt-suggestion tt-header">Programme</div>'
            }
        });

        $('#input-search').bind('typeahead:select', function(ev, suggestion) {
            window.location.replace(suggestion.url);
        });

        $('#input-search').focus();
        $(document).bind('keyup', 'f', function() {
            $('#input-search').focus();
        });
    });
</%block>
