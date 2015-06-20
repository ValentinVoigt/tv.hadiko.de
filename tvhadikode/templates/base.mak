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
                <h1>
                    <%block name="headline">${make_headline()}</%block>
                </h1>
            </div>

            ${self.body()}
        </div>

        <script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>
    </body>
</html>
