
from django.urls import path 
from . import views 


urlpatterns = [
    path('', views.index, name='main'),
    path('summary/', views.kobart_summ, name='summary'),
    path('edit/<str:idx>', views.kobart_edit),
    path('edit/update/', views.edit),
    path('delete/<str:idx>', views.delete),
]
