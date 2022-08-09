from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    #path('', views.IndexView.as_view()),
    path('', views.index.as_view(), name='index'),
    path('<int:category_id>/', views.items.as_view(), name='items'),
    path('<int:category_id>/results/', views.results.as_view(), name='results'),
    path('register/', views.register.as_view(), name='register'),
    path('login/', views.login.as_view(), name='login'),
    path('create_user/', views.create_user, name='create_user'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('<int:category_id>/order/', views.order, name='order'),
    path('auth/', views.auth, name='auth'),
]
