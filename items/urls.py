from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    #path('', views.IndexView.as_view()),
    path('', views.index.as_view(), name='index'),
    path('<int:category_id>/', views.items.as_view(), name='items'),
    path('<int:category_id>/results/', views.results.as_view(), name='results'),
    path('profile/', views.profile, name='profile'),
    path('<int:category_id>/order/', views.order, name='order'),
    path('login/', views.login.as_view(), name='login'),
    path('auth/', views.auth, name='auth'),
]
