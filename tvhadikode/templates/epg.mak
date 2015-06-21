## -*- coding: utf-8 -*-

<%inherit file="base.mak"/>
<%namespace file="functions.mak" import="*"/>
<%block name="title">${make_title()}</%block>
<%block name="headline">${make_headline()}</%block>

<table class="table table-striped" id="epg">
    <thead>
        <tr>
            <th width="35">&nbsp;</th>
            <th width="140">Kanal</th>
            <th>Programm</th>
            <th width="140" class="hidden-xs">Fortschritt</th>
            <th width="180" class="text-right hidden-xs">Stream</th>
        </tr>
    </thead>
    <tbody>
        % for service, current_program, next_program in services:
            <tr>
                <td style="padding-top:15px">
                    % if service.has_logo:
                    <img
                        src="${request.static_path(service.logo_path)}"
                        alt="${service.name} logo" width="35">
                    % endif
                </td>
                <td style="padding-top:15px">
                    <a style="font-size:1.2em;" href="${request.route_path("service", service=service.slug)}">${service.name}</a>
                    <small class="visible-xs">
                        ${watch_service(service, glyphicon=False)}
                    </small>
                </td>
                % if current_program:
                    <td>
                        <a href="#program-${current_program.id}" data-parent="#epg" data-toggle="collapse">
                            ${current_program.name}
                        </a>
                        % if next_program:
                            <br />
                            <small class="text-muted">
                                <span class="visible-xs-inline">
                                    noch ${short_duration(current_program.remaining)}
                                    bis ${smartdate(current_program.end)},
                                </span>
                                danach: ${next_program.name}
                            </small>
                        % endif
                        <div class="collapse" id="program-${current_program.id}">
                            % if current_program.caption:
                                <p><b>${current_program.caption}</b></p>
                            % endif
                            % if current_program.description:
                            <p>
                                ${current_program.description}
                            </p>
                            % endif
                            <p>
                                <span class="text-muted">
                                    von ${smartdate(current_program.start)}
                                    bis ${smartdate(current_program.end)}
                                    (${short_duration(current_program.duration)})
                                </span>
                            </p>
                        </div>
                    </td>
                    <td class="hidden-xs">
                        <div class="progress" style="height:10px; margin:10px 0 0 0">
                            <div
                                class="progress-bar" role="progressbar"
                                aria-valuenow="${current_program.percent_complete}"
                                aria-valuemin="0" aria-valuemax="100"
                                style="width: ${current_program.percent_complete}%;">
                            </div>
                        </div>
                        <small class="text-muted">
                            bis ${smartdate(current_program.end)}
                        </small>
                    </td>
                % else:
                    <td colspan="2"><span class="text-muted">?</span></td>
                % endif
                <td class="text-right hidden-xs">
                    ${watch_service(service)}
                </td>
            </tr>
        % endfor
    </tbody>
</table>
