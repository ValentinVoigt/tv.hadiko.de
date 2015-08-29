## -*- coding: utf-8 -*-

<%inherit file="base_complex.mak"/>
<%namespace file="functions.mak" import="*"/>
<%block name="title">${make_title([service.name])}</%block>
<%block name="headline">${make_headline([service.name])}</%block>


<%block name="javascript">
    ${parent.javascript()}

    $(function() {
        var hash = window.location.hash.substring(1);
        var elem = $('#' + hash);
        if (elem.length != 0) {
            $(elem).find('div.collapse').collapse('show');
            $(window).scrollTo(elem, 800);
        }
    });
</%block>

<% from tvhadikode.utils.group_programs import group_programs %>

<%def name="show_program(title, program, panelclass='default')">
    <div class="panel panel-${panelclass}">
        <div class="panel-heading">
            <h3 class="panel-title">
                ${title}
            </h3>
        </div>
        <div class="panel-body">
            <h4>${program.name}</h4>
            % if program.caption:
                <p><span class="text-muted">${program.caption}</span></p>
            % endif
            % if program.description:
            <p>
                ${program.description}
            </p>
            % endif
            <span class="text-muted">
                von ${smartdate(program.start)}
                bis ${smartdate(program.end)}
                % if program.is_running:
                    (insg. ${short_duration(program.duration)},
                    noch ${short_duration(program.remaining)})
                % else:
                    (insg. ${short_duration(program.duration)},
                    Start in ${short_duration(program.time_until)})
                % endif
            </span>
        </div>
    </div>
</%def>

<div class="row">
    <div class="col-sm-3">
        <div class="panel panel-default">
            <div class="panel-body">
                <span class="thumbnail hidden-xs">
                    <img src="${request.static_path(service.logo_path)}" alt="${service.name} logo">
                </span>
            </div>
            <div class="panel-footer">
                ${watch_service(service)}
            </div>
        </div>
    </div>
    <div class="col-sm-9">

        % if len(service.future_programs) == 0:
            <div class="alert alert-warning" role="alert">
                <strong>Mist!</strong>
                Keine Programminformationen vorhanden.
                <span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span>
            </div>
        % endif

        <%
        current_program = None
        next_program = None
        if len(service.future_programs) > 0:
            current_program = service.future_programs[0]
        if len(service.future_programs) > 1:
            next_program = service.future_programs[1]
        %>

        <div class="row">
            <div class="col-md-6">
                % if current_program:
                    ${show_program("Jetzt live", current_program, "primary")}
                % endif
            </div>
            <div class="col-md-6">
                % if next_program:
                    ${show_program("Im Anschluss", next_program, "info")}
                % endif
            </div>
        </div>

        % for day, programs in group_programs(service.future_programs[2:]):
        <div class="panel panel-default">
            <div class="panel-heading">
                ${day.strftime("%A, %x")}
            </div>
            <table class="table table-hover" style="table-layout:fixed;" id="programs-${day.strftime('%Y%m%d')}">
                % for program in programs:
                    <tr id="p${program.anchor}">
                        <td style="width:140px;">
                            ${smartdate(program.start)}
                            ## ${short_duration(program.duration)}
                            % if program.time_until < 60*60*8:
                                <small class="text-muted">
                                    (in ${short_duration(program.time_until)})
                                </small>
                            % endif
                        </td>
                        <td>
                            <a href="#desc-${program.anchor}" data-parent="#programs-${day.strftime('%Y%m%d')}" data-toggle="collapse">
                                ${program.name}
                            </a>
                            <div class="collapse" id="desc-${program.anchor}">
                                % if program.caption:
                                    <p><span class="text-muted">${program.caption}</span></p>
                                % endif
                                % if program.description:
                                <p>
                                    ${program.description}
                                </p>
                                % endif
                                <p>
                                    <span class="text-muted">
                                        von ${smartdate(program.start)}
                                        bis ${smartdate(program.end)}
                                        (${short_duration(program.duration)})
                                    </span>
                                </p>
                            </div>
                        </td>
                    </tr>
                % endfor
            </table>
        </div>
        % endfor
    </div>
</div>
