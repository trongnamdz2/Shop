from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminPage.as_view(), name='admin'),
    path('additem/', views.PostItem.as_view(), name='additem'),
    path('all-order/', views.AllOrder.as_view(), name='order'),
    path('add-category/', views.AddCategory.as_view(), name='addca'),
    path('created-item/', views.CreatedItem.as_view(), name='createditem'),
    path('process-item/<int:id>', views.ProcessOrder.as_view(), name='process')
]