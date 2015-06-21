## -*- coding: utf-8 -*-

<%inherit file="base.mak"/>
<%namespace file="functions.mak" import="*"/>
<%block name="title">${make_title(["Status"])}</%block>
<%block name="headline">${make_headline(["Status"])}</%block>

<%block name="javascript">
    $(function() {
        $.ajax(
            "${request.route_path('ajax.status.traffic')}"
        ).done(function(data) {
            $('#traffic').html(data);
        }).fail(function() {
            $('#traffic').html($('#error-template').clone().removeClass('hide'));
        });

        $.ajax(
            "${request.route_path('ajax.status.signal_clients')}"
        ).done(function(data) {
            $('#signal_clients').html(data);
        }).fail(function() {
            $('#signal_clients').html($('#error-template').clone().removeClass('hide'));
        });
    });
</%block>

<%def name="ajax_loader()">
    <div class="text-center" style="padding-top:50px;">
        <img alt="Loading..." src="${request.static_path('tvhadikode:static/img/ajax-loader.gif')}">
    </div>
</%def>

<div class="row">
    <div class="col-sm-4">
        <h2 class="page-header">Traffic</h2>
        <div id="traffic">
            ${ajax_loader()}
        </div>
    </div>
    <div class="col-sm-8">
        <div id="signal_clients">
            <h2 class="page-header">Signal</h2>
            ${ajax_loader()}
            <h2 class="page-header">Clients</h2>
            ${ajax_loader()}
        </div>
    </div>
</div>


<div id="error-template" class="alert alert-danger hide" role="alert">
    <strong>Oh nein!</strong>
    Laden fehlgeschlagen! :(
</div>
