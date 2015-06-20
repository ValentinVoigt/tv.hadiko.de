## -*- coding: utf-8 -*-

<%def name="make_title(array=[])">
    HaDiTV
    % for i in array:
        &raquo; ${i}
    % endfor
</%def>

<%def name="make_headline(array=[])">
    <span style="font-size:1.2em;">&raquo;</span>
    % if len(array) > 0:
        <a href="${request.route_path('home')}">
    % endif
    <span style="font-weight:lighter;">HaDi</span><span style="font-size:1.2em;">TV</span>
    % if len(array) > 0:
        </a>
    % endif
    % for i in array:
        <span class="text-muted">&raquo;</span> ${i}
    % endfor
</%def>

<%def name="watch_service(service, glyphicon=True)">
    <a href="${request.route_path('service.watch.multicast', service=service.slug)}">
        % if glyphicon:
            <span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span>
        % endif
        jetzt schauen
    </a>
    &nbsp;
    <small>
        <a href="${request.route_path('service.watch.unicast', service=service.slug)}">
            (alternativ)
        </a>
    </small>
</%def>
