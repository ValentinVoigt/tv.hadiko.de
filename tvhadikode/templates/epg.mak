## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="HaDiNet">
        <link rel="shortcut icon" href="${request.static_url('tvhadikode:static/logo_hadinet_new.png')}">
        <title>TV | HaDiKo</title>
        <link href="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">

        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
        <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="//oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
        <![endif]-->

        <style media="screen">
            .table-valign-middle tbody > tr > td {
                vertical-align: middle;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="page-header">
                <h1>TV <span class="text-muted">|</span> HaDiKo</h1>
            </div>

            <table class="table table-striped table-valign-middle">
                <thead>
                    <tr>
                        <th>Kanal</th>
                        <th>Programm</th>
                        <th>Fortschritt</th>
                        <th>Stream</th>
                    </tr>
                </thead>
                <tbody>
                    % for service in services:
                        <tr>
                            <td>${service.name}</td>
                            % if len(service.future_programs) > 0:
                                <% program = service.future_programs[0] %>
                                <td>
                                    ${program.name}
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
                                            aria-valuenow="${program.percent_complete}"
                                            aria-valuemin="0" aria-valuemax="100"
                                            style="width: ${program.percent_complete}%;">
                                        </div>
                                    </div>
                                    <small class="text-muted">
                                        bis ${smartdate(program.end)}
                                    </small>
                                </td>
                            % else:
                                <td colspan="2"><span class="text-muted">?</span></td>
                            % endif
                            <td>
                                <a href="${request.route_path('watch.multicast', service=service.slug)}">
                                    <span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span>
                                    jetzt schauen
                                </a>
                                <small>
                                    <a href="${request.route_path('watch.unicast', service=service.slug)}">
                                        (alternativ)
                                    </a>
                                </small>
                            </td>
                        </tr>
                    % endfor
                </tbody>
            </table>
        </div>

        <script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>
    </body>
</html>
