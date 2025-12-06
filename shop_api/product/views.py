from  rest_framework.decorators import  api_view
from  rest_framework.response import Response
from  rest_framework import status
from unicodedata import category

from  .models import Category, Product, Review

from .serializers import CategoryListSerializers, CategoryDetailSerializers, ProductListSerializers, \
    ProductDetailSerializers, ReviewListSerializers, ReviewDetailSerializers, ProductReviewListSerializers, \
    CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer


@api_view(http_method_names=['GET', 'POST'])
def category_list_api_view(request):

    if request.method == 'GET':
        categorys = Category.objects.all()
        data = CategoryListSerializers(categorys, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return  Response(status=status.HTTP_400_BAD_REQUEST,
                             data=serializer.errors)

        name = request.data.get('name')
        categorys = Category.objects.create(
            name = name
        )
        categorys.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializers(categorys).data)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        categorys = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = CategoryDetailSerializers(categorys).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        categorys.name = request.data.get('name')
        categorys.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializers(categorys).data)

    elif request.method == 'DELETE':
        categorys.delete()
        return  Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):

    if request.method == 'GET':
        products = Product.objects.select_related('category').all() #1
        data = ProductListSerializers(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')

        products = Product.objects.create(
            title = title,
            description = description,
            price = price,
            category_id = category_id
        )
        products.save()
        return  Response(status=status.HTTP_201_CREATED,
                         data=ProductDetailSerializers(products).data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        products = Product.objects.select_related('category').get(id=id)#2
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ProductDetailSerializers(products).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        products.title  = request.data.get('title')
        products.description =request.data.get('description')
        products.price = request.data.get('price')
        products.category_id = request.data.get('category_id')
        products.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializers(products).data)
    elif request.method == 'DELETE':
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.select_related('product').all()#3
        data = ReviewListSerializers(reviews, many=True).data
        return  Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')

        reviews = Review.objects.create(
            text = text,
            stars = stars,
            product_id = product_id
        )
        reviews.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializers(reviews).data)



@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        reviews = Review.objects.select_related('product').get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewDetailSerializers(reviews).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reviews.text = request.data.get('text')
        reviews.stars = request.data.get('stars')
        reviews.product_id = request.data.get('product_id')
        reviews.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializers(reviews).data)

    elif request.method == 'DELETE':
        reviews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET'])
def product_review_list_api_view(request):
    products = Product.objects.select_related('category').prefetch_related('reviews').all()
    data = ProductReviewListSerializers(products, many=True).data
    return  Response(data=data, status=status.HTTP_200_OK)






