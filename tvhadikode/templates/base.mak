## -*- coding: utf-8 -*-

<%namespace file="functions.mak" import="*"/>

<!DOCTYPE html>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="HaDiNet">
        <link rel="shortcut icon" href="${request.static_path('tvhadikode:static/logo_hadinet_new.png')}">
        <title><%block name="title">${make_title()}</%block></title>
        <link href="${request.static_path('tvhadikode:static/css/bootstrap.min.css')}" rel="stylesheet">
        <link href="${request.static_path('tvhadikode:static/css/lumen-theme.min.css')}" rel="stylesheet">

        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
        <script src="${request.static_path('tvhadikode:static/js/html5shiv.js')}"></script>
        <script src="${request.static_path('tvhadikode:static/js/respond.min.js')}"></script>
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
                <h1>
                    <%block name="headline">${make_headline()}</%block>
                </h1>
            </div>

            ${self.body()}
        </div>

        <script src="${request.static_path('tvhadikode:static/js/jquery.min.js')}"></script>
        <script src="${request.static_path('tvhadikode:static/js/bootstrap.min.js')}"></script>
    </body>
</html>
