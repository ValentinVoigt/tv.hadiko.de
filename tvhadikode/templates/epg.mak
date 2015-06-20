## -*- coding: utf-8 -*-

<%inherit file="base.mak"/>
<%namespace file="functions.mak" import="*"/>
<%block name="title">${make_title()}</%block>
<%block name="headline">${make_headline()}</%block>

<div class="table-responsive">
    <table class="table table-striped table-valign-middle">
        <thead>
            <tr>
                <th class="hidden-xs" width="35">&nbsp;</th>
                <th>Kanal</th>
                <th>Programm</th>
                <th>Fortschritt</th>
                <th>Stream</th>
            </tr>
        </thead>
        <tbody>
            % for service in services:
                <tr>
                    <td class="hidden-xs">
                        % if service.has_logo:
                        <img
                            src="${request.static_path(service.logo_path)}"
                            alt="${service.name} logo" width="35">
                        % endif
                    </td>
                    <td>
                        <a href="${request.route_path("service", service=service.slug)}">${service.name}</a>
                    </td>
                    % if service.current_program:
                        <td>
                            ${service.current_program.name}
                            % if len(service.future_programs) > 1:
                                <br />
                                <small class="text-muted">
                                    Danach: ${service.future_programs[1].name}
                                </small>
                            % endif
                        </td>
                        <td>
                            <div class="progress" style="height:10px; margin:0">
                                <div
                                    class="progress-bar" role="progressbar"
                                    aria-valuenow="${service.current_program.percent_complete}"
                                    aria-valuemin="0" aria-valuemax="100"
                                    style="width: ${service.current_program.percent_complete}%;">
                                </div>
                            </div>
                            <small class="text-muted">
                                bis ${smartdate(service.current_program.end)}
                            </small>
                        </td>
                    % else:
                        <td colspan="2"><span class="text-muted">?</span></td>
                    % endif
                    <td>
                        ${watch_service(service)}
                    </td>
                </tr>
            % endfor
        </tbody>
    </table>
</div>
