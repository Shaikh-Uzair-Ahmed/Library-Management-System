"""
URL configuration for library_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.shortcuts import redirect

handler404 = 'libraryweb.views.error_404'
handler500 = 'libraryweb.views.error_500'


urlpatterns = [
    path('Admin/', admin.site.urls),
    path("", lambda request: redirect("libraryweb:signin")),
    path("Library/", lambda request: redirect("libraryweb:signin")),
    path('Library/', include('libraryweb.urls',namespace='libraryweb'),
    )
    #connected to urls.py of libraryweb app in webpage it will be accessed through library/<webpage-name>
]

