from django.urls import path

from . import views

urlpatterns = [
    path('/', views.index),
    path('/MostPopular/<int:page>',
         views.MostPopular),
    path('/Latest/<int:page>', views.Latest),
    path('/FilterDasboard/<int:year>/', views.FilterDasboard),
    path('/filter/<int:id>', views.filter),
    path('/contributiondepartment/', views.Contributiondepartment),
    path('/submission', views.submission),
    path('/submission/<int:id>', views.submissionPage),
    path('/detail_submission/<int:id>/', views.detail_submission),
    path('/profile', views.profile),
    path('/type', views.TypeContribute),
    path('/addType', views.AddType),
    path('/add', views.Add),
    path('/updateType/<int:id>', views.UpdateType),
    path('/detailType/<int:id>', views.DetailType),
    path('/deleteType/<int:id>', views.DeleteType),
    path('/terms', views.Terms),
    path('/detailTerm/<int:id>', views.DetailTerm),
    path('/updateTerm/<int:id>', views.UpdateTerm),
    path('/deleteTerm/<int:id>', views.DeleteTerm),
    path('/addTerm', views.AddTerm),
    path('/insertTerm', views.InsertTerm),
    path('/comment/<int:id>/', views.comment),

    path('/checkContribute/<int:id>/', views.checkContribute),
]
