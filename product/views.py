from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Review, Product, Category
from .serializers import (
ReviewSerializer, ReviewDetailSerializer,
CategorySerializer, CategoryDetailSerializer, CategorySerializerr,
ProductSerializer, ProductDetailSerializer, ProductSerializerr
)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(data='Review not found!', status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review, many=False).data
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewSerializer(reviews, many=True).data
    return Response(data=list_)

@api_view(['GET'])
def category_list_api_view(request):
    category = Category.objects.all()
    list_ = CategorySerializer(category, many=True).data
    return Response(data=list_)

@api_view(['GET'])
def categories_list_api_view(request):
    category = Category.objects.all()
    list_ = CategorySerializerr(category, many=True).data
    return Response(data=list_)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(data='Category not found!', status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializer(category, many=False).data
    return Response(data=data)


@api_view(['GET'])
def product_list_api_view(request):
    product = Product.objects.all()
    list_ = ProductSerializer(product, many=True).data
    return Response(data=list_)

@api_view(['GET'])
def product_reviews_list_api_view(request):
    product = Product.objects.all()
    list_ = ProductSerializerr(product, many=True).data
    return Response(data=list_)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(data='Product not found!', status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)
