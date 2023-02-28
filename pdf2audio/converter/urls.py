from django.urls import path
from . import views

app_name = 'converter'

urlpatterns = [
    path('', views.home, name='home'),
    path('pdf/<int:pk>/', views.pdf_detail, name='pdf_detail'),
    path('pdf/<int:pk>/download/', views.download_audio, name='download_audio'),
]

