<!DOCTYPE html>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="HaDiNet">
        <link rel="shortcut icon" href="${request.static_url('tvhadikode:static/pyramid-16x16.png')}">
        <title>tv.hadiko.de</title>
        <link href="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">

        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
        <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="//oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
        <![endif]-->
    </head>
    <body>
        <div class="container">
            <div class="page-header">
                <h1>tv.hadiko.de</h1>
            </div>

            % for service in services:
                <h2>
                    ${service.name}
                    <small><a href="${request.route_path('watch.unicast', service=service.slug)}">
                        <span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span>
                        watch now
                    </a></small>
                </h2>
                <ul>
                    % for program in service.future_programs[:10]:
                        <li>
                            % if program.is_running():
                                <span class="label label-info">Live</span>
                            % endif
                            ${program.name} at ${program.start}
                        </li>
                    % endfor
                </ul>
            % endfor
        </div>

        <script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>
    </body>
</html>
