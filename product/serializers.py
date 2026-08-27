from rest_framework import serializers
from .models import Category, Review, Product

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductSerializerr(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = 'title description price category reviews rating'.split()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            total_stars =sum(review.stars for review in reviews)
            return round(total_stars / len(reviews), 2)
        return 0.0

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializerr(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = 'name products_count'.split()

    def get_products_count(self, obj):
        return obj.product_set.count()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'