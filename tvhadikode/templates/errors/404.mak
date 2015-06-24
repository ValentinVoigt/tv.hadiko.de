## -*- coding: utf-8 -*-

<%inherit file="../base.mak"/>
<%namespace file="../functions.mak" import="*"/>
<%block name="title">${make_title(["Fehler"])}</%block>
<%block name="headline">${make_headline(["Fehler"])}</%block>

<div class="row" style="margin-top:100px">
    <div class="col-xs-3">
        <img class="thumbnail img-responsive" alt="Computer meme" src="/static/img/computer-meme-2.png" style="width:100%;">
    </div>
    <div class="col-xs-9" style="line-height:2.5em;">
        <h2>Seite nicht gefunden</h2>
        <p>Leider wurde die aufgerufene Seite nicht gefunden.</p>
        <p>Das tut uns ziemlich leid. Hoffentlich bist du jetzt nicht enttäuscht von uns.</p>
        <p>Falls du das Gefühl hast, dass es sich um einen Fehler handelt, melde dich an <a href="mailto:support@hadiko.de">support@hadiko.de</a>!</p>
    </div>
</div>
