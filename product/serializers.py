from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    def get_products_count(self, obj):
        products = obj.products.all()
        return products.count()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=255)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except:
            raise ValidationError('Product does not exist')
        return product_id

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField() # get_rating()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        total = 0
        count = 0
        for review in reviews:

            if review.stars > 0:
                total += review.stars
                count += 1
        if count == 0:
            return 0
        return total / count

    class Meta:
        model = Product
        fields = 'id title description price category reviews rating'.split()
        # depth = 1

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=255)
    description = serializers.CharField(required=True, min_length=1)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except:
            raise ValidationError('Category does not exist')
        return category_id