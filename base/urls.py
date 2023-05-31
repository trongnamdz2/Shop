from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('', views.HomePage.as_view(), name='home'),
    path('item/<int:pk>/', views.ItemDetail.as_view(), name='detail'),
    path('all/', views.AllItem.as_view(), name='allitem'),
    path('category/<slug:slug>', views.CategoryDetail.as_view(), name='category')
]