from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .models import Service
import requests
# Create your views here.


def main_page(request):
    if request.method == 'GET':
        data = {'name': 'Telenet'}
        return render(request, 'index.html', data)


def about(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT about_us_text FROM about_us")
        about_us_text = cursor.fetchall()
        data = {'text': about_us_text[0][0]}
        return render(request, 'about.html', data)


def contacts(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        refactor_contacts = [str(el[0]) + ':' + str(el[1]) for el in contacts]
        data = {'contacts': refactor_contacts}
        return render(request, 'contacts.html', data)


def services(request, added_new=False):
    services = Service.objects.all()
    services_refactor = [{'id': el.id, 'name': el.name, 'description': el.description, 'price': el.price} for el in services]
    data = {'services': services_refactor, 'added_new': added_new}
    for el in data['services']:
        print(el['description'])
    return render(request, 'services.html', data)


def service_read(request, id):
    service = [el for el in Service.objects.filter(id=id)]
    print(service[0].name)
    data = {'service': service[0]}
    return render(request, 'service_one.html', data)


def service_feedbacks(request, id):
    if request.method == 'GET':
        return render(request, 'new_feedback.html', {'id': id})
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('price'):
            service = Service()
            service.name = request.POST.get('name')
            service.price = request.POST.get('price')
            if request.POST.get('description'):
                service.description = request.POST.get('description')
            service.save()
            data = {'added_new': True}
            return redirect('/services', added_new=True)
        else:
            return HttpResponse(request, '<h1>Метод не поддерживается<h1>')


def services_new(request):
    if request.method == 'GET':
        return render(request, 'new_service.html')
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('price'):
            service = Service()
            service.name = request.POST.get('name')
            service.price = request.POST.get('price')
            if request.POST.get('description'):
                service.description = request.POST.get('description')
            Service.objects.create(service)
            return redirect('/services')
    else:
        return HttpResponse(request, '<h1>Метод не поддерживается<h1>')


def feedbacks_new(request):
    pass
