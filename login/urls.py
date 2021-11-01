from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.login),
    path('forgotPassword', views.forgotPassword),
    path('logout', views.logout),
    path('indexUser', views.indexUser),
    path('Staff', include('staff.urls')),
    path('QAManager', include('QAManager.urls')),
    path('QACoordinator', include('QACoordinator.urls')),
]
