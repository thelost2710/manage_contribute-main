from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('upload/<int:id>/', views.upload),
    path('uploadFile/<int:id>/', views.uploadFile),
    path('UpdateFile/<int:id>/<int:id1>/', views.UpdateFile),
    path('comment/<int:id>/', views.comment),
    path('like/<int:id>/', views.like),
    path('unLike/<int:id>/', views.unLike),
    path('downloadZip/<int:id>/', views.downloadZip),
    path('detail_submission/<int:id>/', views.detail_submission),
    path('editFile/<int:id>/', views.editFile),
    path('deleteFile/<int:id>/', views.deleteFile),

    path('profile', views.profile),
    path('submission', views.submission),
    path('filter/<int:id>/', views.filter),
    path('submission/<int:id>/', views.submissionPage),
    path('ViewClosureDate', views.ViewClosureDate),
]
