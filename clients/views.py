from clients.models import Client
from django.views import View
from django.http import HttpResponse
from datetime import datetime


class Second(View):

    def get(self, request):
        search = request.GET.get("search", None)
        if search is not None:
            clients = Client.objects.filter(surname__icontains=search)
        else:
            clients = Client.objects.all()
        output = ''
        for client in clients:
            output += f'<a href="admin/clients/client/{client.id}/change/">'
            output += f'{client.surname} {client.name} {client.otchestvo} <br />'
            output += '</a>'
        if not len(clients):
            output += f'У нас нет чуваков с такой фамилией <br />'

        output += '<form>'
        output += '<input type="text" name="search">'
        output += '<input type="submit" value="Search">'
        output += '</form>'
        output += '<form action="admin/clients/client/add/">'
        output += '<input type="submit" value="Add">'
        output += '</form>'

        if request.GET.get("ne_hodit", None) is not None:
            Client.objects.filter(pk=request.GET.get("client_id", 0)).update(active=True)
        clients = Client.objects.order_by('date_of_reference').all()
        for client in clients:
            if client.since > 90 and not client.active:
                output += f'{client.surname} {client.name} {client.otchestvo} {client.date_of_reference} '
                output += f'<a href="admin/clients/client/{client.id}/change/">Принесли</a>'
                output += f'<a href="?client_id={client.id}&ne_hodit=1">Ne hodit</a>'
                output += '<br />'

        return HttpResponse(output)



