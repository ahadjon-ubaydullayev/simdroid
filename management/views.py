from django.shortcuts import render
import json
from register.models import SimCardOption, Gift, Client, SimOrder
from .serializers import SimOrderSerializer
from django.http import JsonResponse
from .import service


def orders(request):
    if request.is_ajax and request.method == 'POST':
        if request.POST['action'] == 'add':
            response = service.add_edit_order(request.POST)
            return JsonResponse(response, status=200)
        elif request.POST['action'] == 'delete':
            response = service.delete_order(request.POST)
            return JsonResponse(response, status=200, safe=False)
    if request.method == 'GET':
        if 'add' in request.GET:
            clients = Client.objects.all()
            sims = SimCardOption.objects.all()
            presents = Gift.objects.all()
            context = {'clients':clients,
                        "sims":sims,
                        "presents":presents,
                        }
            return render(request, 'order/add_order.html', context)
        elif 'id' in request.GET:
            clients = Client.objects.all()
            sims = SimCardOption.objects.all()
            presents = Gift.objects.all()
            context = {"order": service.get_order(request.GET['id']),
                        'clients':clients,
                        "sims":sims,
                        "presents":presents,
                        }
            return render(request, 'order/edit_order.html', context=context)
        else:
            return render(request, 'order/main.html')


def clients(request):
    if request.is_ajax and request.method == 'POST':
        if request.POST['action'] == 'add':
            response = service.add_edit_client(request.POST)
            return JsonResponse(response, status=200)
        elif request.POST['action'] == 'delete':
            response = service.delete_client(request.POST)
            return JsonResponse(response, status=200, safe=False)
    if request.method == 'GET':
        if 'add' in request.GET:
            return render(request, 'clients/add_client.html')
        elif 'id' in request.GET:
            context = {"client": service.get_client(request.GET['id'])}
            print(service.get_client(request.GET['id']))
            return render(request, 'clients/edit_client.html', context=context)
        else:
            return render(request, 'clients/list_client.html')

