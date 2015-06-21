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
            <td>${data['name']}</td>
            <td>${data['traffic']} <span class="text-muted">kBit/s</span></td>
        </tr>
        % endfor
    </tbody>
</table>
