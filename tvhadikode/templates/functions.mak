## -*- coding: utf-8 -*-

<%def name="make_title(array=[])">
    TV | HaDiKo
    % for i in array:
        &raquo; ${i}
    % endfor
</%def>

<%def name="make_headline(array=[])">
    TV <span class="text-muted">|</span> HaDiKo
    % for i in array:
        <span class="text-muted">&raquo;</span> ${i}
    % endfor
</%def>
