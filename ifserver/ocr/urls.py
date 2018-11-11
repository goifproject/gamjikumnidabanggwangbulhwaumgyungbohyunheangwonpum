from django.urls import path, include
from . import views


urlpatterns = [
    path('image2text/', views.imageParse, name='image2text'),
    path('image2info/', views.imageAnalysis, name='image2info'),

    path('base2info/', views.base64Analysis, name='base2info'),
]
