from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from rest_framework import status

# Create your views here.

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == "GET":
        # step 1: (QuerySet)
        categories = Category.objects.all()

        # step 2: serializer (many=True)
        data = CategorySerializer(categories, many=True).data
        # step 3: return response
        return Response(
            data=data
        )
    elif request.method == "POST":
        # step 1: recieve data
        name = request.data.get("name")

        # step 2: create category
        category = Category.objects.create(
            name = name,
        )

        # step 3: return response
        return Response(
            status=status.HTTP_201_CREATED,
            #show data after posting
            data=CategorySerializer(category, many=False).data
        )

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except:
        return Response(data={'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = CategorySerializer(category, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(
            status=status.HTTP_200_OK,
            data=CategorySerializer(category, many=False).data
        )

@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = (Product.objects.select_related('category')
                    .prefetch_related('reviews').all())
        # products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        # step 1: recieve data
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')

        # step 2: create product
        product = Product.objects.create(
            title = title,
            description = description,
            price = price,
            category_id = category_id,
        )

        # step 3: return response:
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductSerializer(product, many=False).data
        )

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response(data={'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ProductSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(
            status=status.HTTP_200_OK,
            data=ProductSerializer(product, many=False).data
        )

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        # step 1: collect reviews
        reviews = Review.objects.all()
        # step 2: reformat
        data = ReviewSerializer(reviews, many=True).data
        # step 3: return response
        return Response(data=data)
    elif request.method == 'POST':
        # step 1: recieve data
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')

        # step 2: create review
        review = Review.objects.create(
            text = text,
            stars = stars,
            product_id = product_id,
        )

        # step 3: return response
        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewSerializer(review, many=False).data
        )


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except:
        return Response(data={'error': 'review not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewSerializer(review, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get('product_id')
        review.save()
        return Response(
            status=status.HTTP_200_OK,
            data=ReviewSerializer(review, many=False).data
        )