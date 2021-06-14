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
            output += f'We have {client.surname} with ID {client.id} in our Database <br />'
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

        return HttpResponse(output)


class Spravki(View):

    def get(self, request):
        clients = Client.objects.order_by('date_of_reference').all()
        output = ''
        for client in clients:
            # today = datetime.now()
            # date_spravki = datetime.strptime(Client.date_of_reference.date,  '%Y-%m-%d')
            # if (today-date_spravki).days > 90:
            if client.since > 90:
                output += f'{client.surname} {client.name} {client.otchestvo} {client.date_of_reference} <br />'

        return HttpResponse(output)
