from django.urls import path
from school import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),
    path('new/', views.new),
    path('status/', views.status),
    path('edit_sum/<int:id>/', views.add)
]