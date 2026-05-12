from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer
from rest_framework import status
from django.db import transaction

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
        # step 0: Validation (Existing, Typing, Extra)
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # step 1: recieve data
        name = serializer.validated_data.get("name")

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
        # step 0: Validation (Existing, Typing, Extra)
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        # step 1: recieve validated data
        category.name = serializer.validated_data.get('name')
        # step 2: update existing object
        category.save()
        # step 3: return response
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
        # step 0: Validation (Existing, Typing, Extra)
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        # step 1: recieve data
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')

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
        # step 0: Validation
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        # step 1: Recieve validated data
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        # step 2: update existing object
        product.save()
        # step 3: return response
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
        #step 0: Validation (Existing, Typing, Extra)
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # step 1: recieve data
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')

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
        # step 0: Validate data
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        # step 1: recieve validated data
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        # step 2: update object
        review.save()
        # step 3: return response
        return Response(
            status=status.HTTP_200_OK,
            data=ReviewSerializer(review, many=False).data
        )