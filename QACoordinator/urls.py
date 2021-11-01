from django.urls import path

from . import views

urlpatterns = [
    path('/<int:page>/', views.index),
    path('/1/<int:page>', views.index),
    path('/MostPopular/<int:page>',
         views.MostPopular),
    path('/Latest/<int:page>', views.Latest),
    path('/detail_submission/<int:id>/', views.detail_submission),
    path('/profile', views.profile),
    path('/comment/<int:id>/', views.comment),
]
