from django.core.exceptions import ValidationError
from  rest_framework import  serializers
from  . import  models
from .models import Product, Review, Category
from common.validators import validate_age_user


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

    def validate(self, attrs):
        validate_age_user(self.context['request'])
        return attrs

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

    def validate(self, attrs):
        validate_age_user(self.context['request'])
        return attrs

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'

    def validate(self, attrs):
        validate_age_user(self.context['request'])
        return attrs




class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'products_count']


class CategoryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductListSerializers(serializers.ModelSerializer):
    category =serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductDetailSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = '__all__'


class ReviewListSerializers(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = models.Review
        fields = '__all__'

class ReviewDetailSerializers(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = models.Review
        fields = '__all__'



class ProductReviewListSerializers(serializers.ModelSerializer):
    reviews = ReviewListSerializers(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews', 'average_stars']


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError("Category does not exist!")
        return category_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    stars = serializers.IntegerField(max_value=5, min_value=1)
    product_id = serializers.IntegerField()

    def validate_product_id(self,product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Product does not exist!")
        return product_id






