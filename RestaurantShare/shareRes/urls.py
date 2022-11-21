from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('restaurantDetail/', views.restaurantDetail, name='resDetailPage'),
	path('restaurantCreate/', views.restaurantCreate, name='resCrestaPage'),
	path('categoryCreate/', views.categoryCreate, name='cateCreatePate'),
	path('categoryCreate/create', views.Create_category, name='cateCreate'),
]