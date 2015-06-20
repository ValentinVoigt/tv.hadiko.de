## -*- coding: utf-8 -*-

<%inherit file="base.mak"/>
<%namespace file="functions.mak" import="*"/>
<%block name="title">${make_title([service.name])}</%block>
<%block name="headline">${make_headline([service.name])}</%block>

<%def name="show_program(title, program, panelclass='default')">
    <div class="panel panel-${panelclass}">
        <div class="panel-heading">
            <h3 class="panel-title">
                ${title}
            </h3>
        </div>
        <div class="panel-body">
            <h4>${program.name}</h4>
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
        <span class="thumbnail hidden-xs">
            <img src="${request.static_path(service.logo_path)}" alt="${service.name} logo">
        </span>

        <div class="panel panel-default">
            <div class="panel-body">
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

        <div class="row">
            <div class="col-md-6">
                % if service.current_program:
                    ${show_program("Jetzt live", service.current_program, "primary")}
                % endif
            </div>
            <div class="col-md-6">
                % if len(service.future_programs) > 1:
                    ${show_program("Im Anschluss", service.future_programs[1], "info")}
                % endif
            </div>
        </div>

        <div class="panel panel-default">
            <div class="panel-heading">
                Aussicht
            </div>

            <table class="table table-hover" style="table-layout:auto; width:100%;">
                % for program in service.future_programs[2:]:
                    <tr>
                        <td>
                            ${smartdate(program.start)}
                            ## ${short_duration(program.duration)}
                            % if program.time_until < 60*60*8:
                                <small class="text-muted">
                                    (in ${short_duration(program.time_until)})
                                </small>
                            % endif
                        </td>
                        <td>${program.name}</td>
                    </tr>
                % endfor
            </table>
        </div>
    </div>
</div>
