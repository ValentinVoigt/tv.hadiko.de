## -*- coding: utf-8 -*-

<table class="table table-striped table-hover">
    <thead>
        <tr>
            <th>Kanal</th>
            <th>Traffic</th>
        </tr>
    </thead>
    <tbody>
        % for data in traffics:
        <tr>
            <td>
                % if services.get(data.get('name')):
                <a href="${request.route_path('service', service=services.get(data.get('name')).slug)}">${data['name']}</a>
                % else:
                ${data['name']}
                % endif
            </td>
            <td>${data['traffic']} <span class="text-muted">kB/s</span></td>
        </tr>
        % endfor
    </tbody>
</table>
