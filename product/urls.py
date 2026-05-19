from django.urls import path, include
from . import views

urlpatterns = [
    path('categories/', views.category_list_api_view),
    path('categories/<int:pk>/', views.category_detail_api_view),

    path('products/', views.product_list_api_view),
    path('products/<int:pk>/', views.product_detail_api_view),

    path('reviews/', views.review_list_api_view),
    path('reviews/<int:pk>/', views.review_detail_api_view),

]
