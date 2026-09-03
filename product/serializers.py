from rest_framework import serializers
from .models import Category, Review, Product
from rest_framework.exceptions import ValidationError

class StrictCharField(serializers.CharField):
    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise serializers.ValidationError('the field only accepts text')
        return super().to_internal_value(data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewValidator(serializers.Serializer):
    text = StrictCharField(min_length=1, max_length=255)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        product_id = product_id['product_id']
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist')

        return product_id


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

class ProductValidator(serializers.Serializer):
    title = StrictCharField(min_length=1, max_length=255)
    description = StrictCharField()
    price = serializers.IntegerField()
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        category_id = category_id['category_id']
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist')
        return category_id


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

class CategoryValidator(serializers.Serializer):
    name = StrictCharField(min_length=1, max_length=255)
