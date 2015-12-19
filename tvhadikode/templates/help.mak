## -*- coding: utf-8 -*-

<%inherit file="base_complex.mak"/>
<%namespace file="functions.mak" import="*"/>
<%block name="title">${make_title(["Anleitung und Tipps"])}</%block>
<%block name="headline">${make_headline(["Anleitung und Tipps"])}</%block>

<h2 style="margin:1em 0">Einzelne Sender</h2>

<img src="${request.static_path('tvhadikode:static/img/vlc.png')}" alt="VLC Logo"
    class="pull-left hidden-xs img-responsive" style="height:120px; margin:0 1em 1em 1em" />

<p>
    Wir empfehlen den <a href="https://www.videolan.org/vlc/" target="_blank">VLC Player</a>, um die
    TV Livestreams im HaDiKo zu schauen. Mit diesem kannst du die <code>m3u</code>-Dateien öffnen, die
    du hier herunterladen kannst.
</p>

<p>
    Der <i>„Jetzt schauen“</i>-Link bringt dich zum sogenannten Multicast Stream. Dieser hilft uns
    Traffic zu sparen und die Serverlast gering zu halten. Es kann allerdings passieren, dass dieser
    bei dir nicht funktioniert. Falls das der Fall ist, verwende stattdessen den
    <i>„alternativ“</i>-Link.
</p>

<p>
    Wenn dein Browser dich fragt, womit er die <code>m3u</code>-Dateien öffnen soll, dann kannst du
    in diesem Fenster den VLC-Player auswählen. Im Google Chrome kannst du einen Rechtsklick auf
    deinen Download machen und dort <i>„Dateien dieses Typs immer öffnen“</i>. Wenn du das
    eingestellt hast, kannst du bequem mit nur einem Klick Fernsehen und umschalten!
</p>

<p>
    Solltest du Fragen oder Probleme mit der Einrichtung haben, so melde dich gern an
    <a href="mailto:support@hadiko.de">support@hadiko.de</a> oder schau bei uns im IRC vorbei unter
    <samp>irc.hadiko.de</samp> im Channel <samp>#help</samp>.
</p>

<br style="clear:both">

<h2 style="margin-bottom:1em">Bequem alle Sender speichern</h2>

<img src="${request.static_path('tvhadikode:static/img/kodi.png')}" alt="Kodi Logo"
    class="pull-right hidden-xs img-responsive" style="height:120px; margin:0 1em 1em 1em" />

<p>
    Wenn du nicht jedes mal auf die Webseite zugreifen möchtest, kannst du dir die Playlist für alle
    Sender herunterladen und speichern. Anschließend genügt ein Doppelklick auf diese Playlist, um
    den VLC mitsamt allen Sendern zur Auswahl zu öffnen.
</p>

<blockquote>
    <p>
        Multicast Playlist: <samp><a href="${request.route_path("watch.multicast")}">tv_multicast.m3u</a></samp>
    </p>
    <p>
        Unicast Playlist: <samp><a href="${request.route_path("watch.unicast")}">tv_unicast.m3u</a></samp>
    </p>
    <p>
        <span class="text-muted">(Rechtsklick → Link speichern unter...)</span>
    </p>
</blockquote>

<p>
    Diese Playlists eignen sich auch zum Import in das Mediacenter
    <a href="http://kodi.tv/" target="_blank">Kodi</a>. Dazu installierst du den
    <a href="http://kodi.wiki/view/Add-on:IPTV_Simple_Client" target="_blank">PVR IPTV Simple Client</a>
    als Addon. Bei der Konfiguration kannst du dann eine der beiden Playlist-URLs
    <span class="text-muted">(Rechtsklick → Adresse des Links kopieren)</span> unter dem Punkt
    <i>„M3U Wiedergabelisten-URL“</i> einfügen. Anschließend kannst du unter
    <i>„Basis-URL der Senderlogos“</i> noch <samp>http://tv.hadiko.de</samp> eintragen, um auch die Senderlogos
    zu sehen. Im Feld <i>„XMLTV URL“</i> trägst du dann noch <samp>http://tv.hadiko.de/playlist/xmltv.xml</samp>
    ein, um auch ein EPG in deinem Kodi zu sehen.
</p>

<br style="clear:both">
