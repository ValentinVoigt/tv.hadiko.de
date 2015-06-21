## -*- coding: utf-8 -*-

<h2 class="page-header">Signal</h2>

<table class="table table-striped table-hover">
    <thead>
        <tr>
            <th>Card</th>
            <th>System</th>
            <th>Frequenz</th>
            <th>SNR</th>
            <th>Stärke</th>
            <th>#Kanäle</th>
        </tr>
    </thead>
    <tbody>
        % for data in status:
        <tr>
            <td>${data['tune']['card_path']}</td>
            <td>${data['tune']['frontend_system']}</td>
            <td>${data['tune']['frontend_frequency']}</td>
            <td>${data['tune']['frontend_signal']}</td>
            <td>${data['tune']['frontend_snr']}</td>
            <td>${len(data['channels'])}</td>
        </tr>
        % endfor
    </tbody>
</table>

<h2 class="page-header">Clients</h2>

<% n = 0 %>

<table class="table table-striped table-hover">
    <thead>
        <tr>
            <th>Kanal</th>
            <th>Clients</th>
        </tr>
    </thead>
    <tbody>
        % for data in status:
        % for channel in data['channels']:
        <% if len(channel['clients'][0].keys()) == 0: continue %>
        <% n+= 1 %>
        <tr>
            <td>${channel['name']}</td>
            <td>
                <ul class="list-unstyled">
                % for client in channel['clients']:
                    <li>${client['remote_address']}</li>
                % endfor
                </ul>
            </td>
        </tr>
        % endfor
        % endfor

        % if n == 0:
            <tr class="info">
                <td colspan="2">
                    <strong>Niemand</strong>
                    schaut gerade (via unicast)!
                </td>
            </tr>
        % else:
        <tfoot>
            <tr>
                <td colspan="2">
                    <strong>Hinweis</strong> Nur Unicast Clients können angezeigt werden.
                </td>
            </td>
        </tfoot>
        % endif
    </tbody>
</table>
