from django.urls import path, include

urlpatterns = [
    path('ocr/', include('ocr.urls')),
]

