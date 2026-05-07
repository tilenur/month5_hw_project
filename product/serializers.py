from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    def get_products_count(self, obj):
        products = obj.products.all()
        return products.count()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()

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


