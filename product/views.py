from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Review, Product, Category
from .serializers import (
ReviewSerializer, ReviewDetailSerializer, ReviewValidator,
CategorySerializer, CategoryDetailSerializer, CategorySerializerr, CategoryValidator,
ProductSerializer, ProductDetailSerializer, ProductSerializerr, ProductValidator
)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(data='Review not found!', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(data=data)
    if request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        validator = ReviewValidator(data=request.data)
        if not validator.is_valid():
            return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
        validated = validator.validated_data

        review.text = validated.data['text']
        review.stars = validated.data['stars']
        review.product_id = validated.data['product_id']
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        list_ = ReviewSerializer(review, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        validator = ReviewValidator(data=request.data)
        if not validator.is_valid():
            return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
        validated = validator.validated_data

        text = validated.data['text']
        product_id = validated.data['product_id']
        stars = validated.data['stars']
    review = Review.objects.create(text=text, product_id=product_id, stars=stars)
    return Response(status=status.HTTP_201_CREATED,
                    data=ReviewDetailSerializer(review).data)

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        category = Category.objects.all()
        list_ = CategorySerializer(category, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        validator = CategoryValidator(data=request.data)
        if not validator.is_valid():
            return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
        validated = validator.validated_data
        name = validated.data['name']
    category = Category.objects.create(name=name)

    return Response(status=status.HTTP_201_CREATED,
                    data=CategoryDetailSerializer(category).data)


@api_view(['GET'])
def categories_list_api_view(request):
    category = Category.objects.all()
    list_ = CategorySerializerr(category, many=True).data
    return Response(data=list_)

@api_view(['GET', 'DELETE', 'PUT'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(data='Category not found!', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializer(category, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        validator = CategoryValidator(data=request.data)
        if not validator.is_valid():
            return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
        validated = validator.validated_data
        category.name = validated.data['name']
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)



@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        list_ = ProductSerializer(product, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        validator = ProductValidator(data=request.data)
        if not validator.is_valid():
            return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
        validated = validator.validated_data

        title = validated.data['title']
        description = validated.data['description']
        price = validated.data['price']
        category_id = validated.data['category_id']

        product = Product.objects.create(title=title,
                                         description=description,
                                         price=price,
                                         category_id=category_id)
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)

@api_view(['GET'])
def product_reviews_list_api_view(request):
    product = Product.objects.all()
    list_ = ProductSerializerr(product, many=True).data
    return Response(data=list_)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(data='Product not found!', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        validator = ProductValidator(data=request.data)
        if not validator.is_valid():
            return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
        validated = validator.validated_data

        product.title = validated.data['title']
        product.description = validated.data['description']
        product.price = validated.data['price']
        product.category_id = validated.data['category_id']
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
