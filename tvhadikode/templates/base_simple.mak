## -*- coding: utf-8 -*-

<%namespace file="functions.mak" import="*"/>

<!DOCTYPE html>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="HaDiNet">
        <link rel="shortcut icon" href="${request.static_path('tvhadikode:static/img/logo_hadinet_small.png')}">
        <title><%block name="title">${make_title()}</%block></title>
        <link href="${request.static_path('tvhadikode:static/css/bootstrap.min.css')}" rel="stylesheet">
        <link href="${request.static_path('tvhadikode:static/css/lumen-theme.min.css')}" rel="stylesheet">
        <link href="${request.static_path('tvhadikode:static/css/typeahead-theme.css')}" rel="stylesheet">
        <link href="${request.static_path('tvhadikode:static/css/main.css')}" rel="stylesheet">

        <!--[if lt IE 9]>
        <script src="${request.static_path('tvhadikode:static/js/html5shiv.js')}"></script>
        <script src="${request.static_path('tvhadikode:static/js/respond.min.js')}"></script>
        <![endif]-->
    </head>
    <body>
        <div class="container" id="main">
            <div class="page-header" id="header">
                <div class="row">
                    <div class="col-sm-8">
                        <h1><%block name="headline">${make_headline()}</%block></h1>
                    </div>
                    <div class="col-sm-4">
                        <%block name="header">
                            <img src="${request.static_path('tvhadikode:static/img/logo_hadinet_light.png')}"
                                alt="HaDiNet Logo"  class="pull-right" />
                        </%block>
                    </div>
                </div>
            </div>

            ${self.body()}
        </div>

        <footer class="footer">
            <div class="container">
                <div class="row">
                    <div class="col-xs-4">
                        <p>
                            <a href="mailto:support@hadiko.de">support@hadiko.de</a>
                        </p>
                    </div>
                    <div class="col-xs-4">
                        <p class="text-muted text-center">
                            &copy; 2015, HaDiNet
                        </p>
                    </div>
                    <div class="col-xs-4">
                        <img src="${request.static_path('tvhadikode:static/img/logo_hadinet_light.png')}"
                                alt="HaDiNet Logo" class="pull-right" />
                    </div>

                </div>
            </div>
        </footer>
        <script src="${request.static_path('tvhadikode:static/js/jquery.min.js')}"></script>
        <script src="${request.static_path('tvhadikode:static/js/bootstrap.min.js')}"></script>
        <script src="${request.static_path('tvhadikode:static/js/jquery.scrollTo.min.js')}"></script>
        <%block name="javascript_src"/>
        <script type="text/javascript">
            <%block name="javascript"/>
        </script>
    </body>
</html>
