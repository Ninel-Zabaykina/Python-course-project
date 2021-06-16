from clients.models import Client
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render


class Second(View):

    def get(self, request):
        search = request.GET.get("search", None)
        if search is not None:
            clients = Client.objects.filter(surname__icontains=search)
        else:
            clients = Client.objects.all()
        output = ''

        output += '<form class="form-inline">'
        output += '<input type="text" name="search" class="form-control mb-2" style="width:88%;">'
        output += '<input type="submit" value="Найти" class="btn btn-primary mb-2">'
        output += '</form>'

        if request.GET.get("ne_hodit", None) is not None:
            Client.objects.filter(pk=request.GET.get("client_id", 0)).update(active=True)
        clients = Client.objects.order_by('date_of_reference').all()
        for client in clients:
            if client.since > 90 and not client.active:
                output += '<div class="alert alert-danger" role="alert">'
                output += f'{client.surname} {client.name} {client.otchestvo} {client.date_of_reference}'
                output += f'<a href="admin/clients/client/{client.id}/change/" class="btn btn-success" style="margin-left:120px ">Принесли</a>'
                output += f'<a href="?client_id={client.id}&ne_hodit=1" class="btn btn-danger" style="float:right;">Не ходит</a>'
                output += '</div>'



        output += '<div></div>'
        output += '''<table class="table table-striped">
                    <thead>
                    <tr>
                      <th scope="col">Фамилия</th>
                      <th scope="col">Имя</th>
                      <th scope="col">Oтчество</th>
                    </tr>
                  </thead>
                  <tbody>'''
        for client in clients:
            output += '<tr>'
            output += '<td>'
            output += f'<a href="admin/clients/client/{client.id}/change/">'
            output += f'{client.surname} <br />'
            output += '</a>'
            output += '</td>'

            output += '<td>'
            output += f'<a href="admin/clients/client/{client.id}/change/">'
            output += f'{client.name}<br />'
            output += '</a>'
            output += '</td>'

            output += '<td>'
            output += f'<a href="admin/clients/client/{client.id}/change/">'
            output += f'{client.otchestvo} <br />'
            output += '</a>'
            output += '</td>'

            output += '</tr>'
        output += '</tbody></table>'

        if not len(clients):
            output += f'У нас нет клиентов с такой фамилией <br />'

        output += '<div style="margin:0 auto;width:220px;"><form action="admin/clients/client/add/">'
        output += '<input type="submit" class="btn btn-warning" value="Добавить нового клиента">'
        output += '</form></div>'

        # return HttpResponse(output)
        return render(request, 'general.html', context={'output': output})


