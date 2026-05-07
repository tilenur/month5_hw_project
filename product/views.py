from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def category_list_api_view(request):
    # step 1: (QuerySet)
    categories = Category.objects.all()

    # step 2: serializer (many=True)
    data = CategorySerializer(categories, many=True).data
    # step 3: return response
    return Response(
        data=data
    )

@api_view(['GET'])
def category_detail_api_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except:
        return Response(data={'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
    data = CategorySerializer(category, many=False).data
    return Response(data=data)

@api_view(['GET'])
def product_list_api_view(request):
    products = (Product.objects.select_related('category')
                .prefetch_related('reviews').all())
    # products = Product.objects.all()
    data = ProductSerializer(products, many=True).data
    return Response(data=data)

@api_view(['GET'])
def product_detail_api_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response(data={'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
    data = ProductSerializer(product, many=False).data
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except:
        return Response(data={'error': 'review not found'}, status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review, many=False).data
    return Response(data=data)