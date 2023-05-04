"""app_telenet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from telenet_site.views import main_page, about, contacts, services, services_new, \
    service_feedbacks_new, service_photo_add, \
    service_read, service_feedbacks, service_edit, delete_service, delete_feedback, UploadExcelView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name="main_page"),
    path('contacts/', contacts, name="contacts"),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('services/new', services_new, name='services'),
    path('service/feedbacks/<int:id>', service_feedbacks, name='service_feedbacks'),
    path('service/<int:id>', service_read, name='service_read'),
    path('service/edit/<int:id>', service_edit, name='service_edit'),
    path('service/feedbacks/new/<int:id>', service_feedbacks_new, name='service_feedbacks_new'),
    path('service/photo/add/<int:id>', service_photo_add, name='service_photo_add'),
    path('service/feedbacks/delete/<int:id>', delete_feedback, name='service_feedbacks_delete'),
    path('service/delete/<int:id>', delete_service, name='delete_service'),
    path('services/upload_from_file', UploadExcelView.as_view(), name='fill_service_from_excel')
]
