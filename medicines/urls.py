from . import views
from django.urls import path


urlpatterns = [
    path('create/',views.medicine_create,name='createmedicine'),
    path('read/',views.medicine_read,name='readmedicine'),
    path('update/<int:id>/',views.medicine_update,name='updatemedicine'),
    path('delete/<int:pk>',views.medicine_delete,name='deletemedicine'),     
    
    
]