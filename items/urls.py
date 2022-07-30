from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:category_id>/', views.items, name='items'),
]
