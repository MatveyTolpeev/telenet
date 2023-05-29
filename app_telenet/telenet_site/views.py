from django.forms import model_to_dict
from rest_framework import generics
from PIL import Image
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from django.db.models import Avg
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ServiceImageSetForm
from .models import Service, Feedback
from .other_functions import out_green, out_blue, out_yellow
from .serializers import ServiceSerializer
from .tasks import fill_service_from_excel
import requests


def main_page(request):
    out_yellow('[+] main_page')
    if request.method == 'GET':
        data = {'name': 'Telenet'}
        out_green('[++] end main_page')
        return render(request, 'index.html', data)


def about(request):
    out_yellow('[+] about')
    with connection.cursor() as cursor:
        cursor.execute("SELECT about_us_text FROM about_us")
        about_us_text = cursor.fetchall()
        data = {'text': about_us_text[0][0]}
        out_green('[++] end about')
        return render(request, 'about.html', data)


def contacts(request):
    out_yellow('[+] contacts')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        refactor_contacts = [str(el[0]) + ':' + str(el[1]) for el in contacts]
        data = {'contacts': refactor_contacts}
        out_green('[++] end contacts')
        return render(request, 'contacts.html', data)


def services(request, added_new=False):
    out_yellow('[+] services')
    # services = Service.objects.all()
    services = Service.objects.annotate(avg_score=Avg('feedback__score'))
    service_refactor = []
    try:
        services_refactor = [{'id': el.id, 'name': el.name, 'description': el.description, 'price': el.price,
                              'avg_score': round(el.avg_score, 2)} for el in services]
    except Exception as e:
        services_refactor = [{'id': el.id, 'name': el.name, 'description': el.description, 'price': el.price}
                            for el in services]
    data = {'services': services_refactor, 'added_new': added_new}
    out_green('[++] end services')
    return render(request, 'services.html', data)


def service_read(request, id):
    out_yellow('[+] service_read')
    service = [el for el in Service.objects.filter(id=id)]
    print(service[0].name)
    data = {'service': service[0]}
    out_green('[++] end service_read')
    return render(request, 'service_one.html', data)


def service_feedbacks(request, id):
    out_yellow('[+] service_feedbacks')
    if request.method == 'GET':
        feedbacks = Feedback.objects.filter(service=id)
        service = Service.objects.filter(id=id)
        feedbacks_rendered = [el for el in feedbacks]
        services_names = [el.name for el in service]
        service_name = services_names[0]
        data = {'feedbacks': feedbacks_rendered, 'service_name': service_name, }
        out_green('[++] end service_feedbacks')
        return render(request, 'service_feedbacks.html', data)
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('price'):
            service = Service()
            service.name = request.POST.get('name')
            service.price = request.POST.get('price')
            if request.POST.get('description'):
                service.description = request.POST.get('description')
            service.save()
            data = {'added_new': True}
            out_green('[++] end service_feedbacks')
            return redirect('/services', data)
        else:
            out_green('[++] end service_feedbacks')
            return HttpResponse(request, '<h1>Метод не поддерживается<h1>')


def services_new(request):
    out_yellow('[+] services_new')
    if request.method == 'GET':
        out_green('[++] end services_new')
        return render(request, 'new_service.html')
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('price'):
            service = Service()
            service.name = request.POST.get('name')
            service.price = request.POST.get('price')
            if request.POST.get('description'):
                service.description = request.POST.get('description')
            service.save()
            out_green('[++] end services_new')
            return redirect('/services')
    else:
        out_green('[++] end services_new')
        return HttpResponse(request, '<h1>Метод не поддерживается<h1>')


def service_edit(request, id):
    out_yellow('[+] service_edit')
    if request.method == 'GET':
        service = Service.objects.get(id=id)
        data = {'service': service}
        out_green('[++] end service_edit')
        return render(request, 'service_edit.html', data)
    if request.method == 'POST':
        service = Service.objects.get(id=id)
        print('{}, {}, {}'.format(str(request.POST.get('price')), str(request.POST.get('description')),
                                  str(request.POST.get('name'))))
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.save()
        return redirect('/services')


def service_feedbacks_new(request, id):
    out_yellow('[+] service_feedbacks_new')
    if request.method == 'GET':
        out_green('[++] end service_feedbacks_new')
        return render(request, 'new_feedback.html', {'id': id})
    if request.method == 'POST':
        print(type(id))
        feedback = Feedback()
        feedback.text = request.POST.get('text')
        feedback.score = request.POST.get('score')
        feedback.service = Service.objects.get(id=id)
        feedback.save()
        context = {'my_variable': 'Hello, world!'}
        out_green('[++] end service_feedbacks_new')
        return redirect('/service/feedbacks/' + str(id))


def delete_feedback(request, id):
    out_yellow('[+] delete_feedback')
    feed = Feedback.objects.get(id=id)
    temp_feed = feed
    feed.delete()
    data = {'message': 'Вы удалили отзыв: ' + str(temp_feed.text) + ' с оценкой: ' + str(temp_feed.score)}
    out_green('[++] end delete_feedback')
    return redirect('/service/feedbacks/' + str(temp_feed.service_id), deleted=data)
    # return redirect('service_feedbacks', id=temp_feed.service_id, deleted=data)


def delete_service(request, id):
    out_yellow('[+] delete_service')
    serv = Service.objects.get(id=id)
    temp_serv = serv
    serv.delete()
    data = {'message': 'Вы удалили услугу: ' + str(temp_serv.description) + ' с ценой: ' + str(temp_serv.price)}
    out_green('[++] end delete_service')
    return redirect('/services', deleted=data)


def service_photo_add(request, id):
    out_yellow('[+] service_photo_add')
    if request.method == 'POST':
        form = ServiceImageSetForm(request.POST, request.FILES)
        if form.is_valid():
            # Получаем изображение из формы
            image = form.cleaned_data['image']
            # Открываем изображение с помощью Pillow
            img = Image.open(image)
            # Сжимаем изображение до размера 150x100
            img.thumbnail((200, 150))
            # Сохраняем изображение в модели
            service = Service.objects.get(id=id)
            service.image = img
            print(service.image)
            service.save()
            # Выводим изображение на экран
            out_green('[++] end main_page')
            return redirect('/services')
    else:
        form = ServiceImageSetForm()
    out_green('[++] end service_photo_add')
    return render(request, 'service_upload_image.html', {'form': form})


class UploadExcelView(View):
    def get(self, request):
        return render(request, 'upload_excel.html')

    def post(self, request):
        file = request.FILES.get('file')
        print(file)
        if file:
            fill_service_from_excel.delay(file.temporary_file_path())
            return HttpResponse('File uploaded and processing started. '
                                '<a href="/services"><button>Вернуться на главную страницу</button></a>')
        else:
            return HttpResponse(
                'No file uploaded. <a href="/services"><button>Вернуться на главную страницу</button></a>')


# Далее идёт API на DRF


class ServiceApiView(APIView):
    def get(self, request):
        lst = Service.objects.all().values()
        return Response({'posts': list(lst)})

    def post(self, request):
        service_new = Service.objects.create(
            name=request.data['name'],
            description=request.data['description'],
            price=request.data['price'],
            image=None
        )

        return Response({'post': model_to_dict(service_new)})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed without id"})

        try:
            instance = Service.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = ServiceSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "Success"})
