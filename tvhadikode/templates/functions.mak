## -*- coding: utf-8 -*-

<%def name="make_title(array=[])">
    TV | HaDiKo
    % for i in array:
        &raquo; ${i}
    % endfor
</%def>

<%def name="make_headline(array=[])">
    % if len(array) > 0:
        <a href="${request.route_path('home')}">
    % endif
    TV <span class="text-muted">|</span> HaDiKo
    % if len(array) > 0:
        </a>
    % endif
    % for i in array:
        <span class="text-muted">&raquo;</span> ${i}
    % endfor
</%def>

<%def name="watch_service(service)">
    <a href="${request.route_path('service.watch.multicast', service=service.slug)}">
        <span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span>
        jetzt schauen
    </a>
    <small>
        <a href="${request.route_path('service.watch.unicast', service=service.slug)}">
            (alternativ)
        </a>
    </small>
</%def>
