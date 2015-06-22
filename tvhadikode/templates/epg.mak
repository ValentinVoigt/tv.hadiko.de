## -*- coding: utf-8 -*-

<%inherit file="base.mak"/>
<%namespace file="functions.mak" import="*"/>
<%block name="title">${make_title()}</%block>
<%block name="headline">${make_headline()}</%block>

<%block name="javascript">
    function update_programs_loop() {
        update_programs(true);
        window.setTimeout(update_programs_loop, 3000);
    }
    function update_programs(do_reload) {
        var rows_to_update = new Array();
        $('.progress-bar.program').each(function() {
            var start = Date.parse($(this).data('start'));
            var end = Date.parse($(this).data('end'));
            var now = new Date().getTime();
            var duration = Math.round((end - start) / 1000);
            var elapsed = Math.round((now - start) / 1000);
            var percentage = Math.round(elapsed / duration * 100);
            if (now >= end)
                rows_to_update.push($(this).closest("tr"));
            if (percentage > 100)
                percentage = 100;
            $(this).attr("aria-valuenow", percentage).css("width", percentage + "%");
        });
        if (rows_to_update.length > 0 && do_reload)
            reload_rows(rows_to_update);
    }

    function display_loader(row, dfd) {
        $(row).css("height", $(row).height() + "px");
        var loader = $('<td><img style="margin-top:15px;" alt="Loading..."></td>');
        loader.find('img').attr('src', $('#epg').data('loader-src'));

        $(row).find("td:eq(2), td:eq(3)").fadeOut(function() {
            $(this).replaceWith(loader.clone());
            dfd.resolve();
        });
    }

    function reload_rows(rows) {
        var dfd = $.Deferred();

        var slugs = new Array();
        $(rows).each(function() {
            display_loader($(this), dfd);
            slugs.push($(this).data('service-slug'));
        });

        $.ajax({
            method: "POST",
            url: $('#epg').data('reload-url'),
            dataType: 'json',
            data: {'services': slugs}
        }).fail(function(jqXHR, textStatus, errorThrown) {
            var error = $('<td style="padding-top:15px"><strong>Fehler!</strong> Laden fehlgeschlagen! <span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span></td>');
            $(rows).each(function() {
                $(this).find("td:eq(2)").replaceWith(error.clone());
                $(this).find("td:eq(3)").replaceWith("<td></td>");
            });
        }).done(function(data_raw, textStatus, jqXHR) {
            dfd.done(function() {
                for (var slug in data_raw.rows) {
                    var data = $(data_raw.rows[slug]).clone();
                    $(data).find('td:eq(2), td:eq(3)').hide();

                    $("#service-"+slug).replaceWith(data);
                    $(data).find('td:eq(2), td:eq(3)').fadeIn(function() {
                        update_programs(false);
                    });
                }
            });
        });
    }

    $(function() {
        update_programs_loop();
    });
</%block>

<%def name="service_row(service, current_program, next_program)">
    <tr class="epgrow" data-service-slug="${service.slug}" id="service-${service.slug}">
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
            <%
            from datetime import timedelta, datetime
            %>
            <td class="hidden-xs">
                <div class="progress" style="height:10px; margin:10px 0 0 0">
                    <div
                        class="progress-bar program" role="progressbar"
                        data-start="${current_program.start_utc.isoformat()}"
                        data-end="${current_program.end_utc.isoformat()}"
                        aria-valuenow="0"
                        aria-valuemin="0" aria-valuemax="100"
                        style="width: 0%;">
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
</%def>

<table class="table table-striped" id="epg"
    data-loader-src="${request.static_path('tvhadikode:static/img/ajax-loader.gif')}"
    data-reload-url="${request.route_path("ajax.epg_update")}">
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
            ${service_row(service, current_program, next_program)}
        % endfor
    </tbody>
</table>
