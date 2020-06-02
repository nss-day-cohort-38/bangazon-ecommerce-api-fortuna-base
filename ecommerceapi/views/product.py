from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name = 'product',
            lookup_field = 'id'
        )
        fields = ('id', 'url', 'title', 'price', 'description', 'quantity','location', 'image_path', 'product_type_id')
        depth = 1
class Products(ViewSet):

    def create(self, request):
        new_product = Product()
        new_product.title = request.data['title']
        new_product.price = request.data['price']
        new_product.description = request.data['description']
        new_product.quantity = request.data['quantity']
        new_product.customer = request.auth.user.customer
        new_product.location = request.data['location']
        new_product.image_path = request.data['image_path']
        new_product.product_type_id = request.data['product_type_id']
        new_product.save()

        serializer = ProductSerializer(new_product, context = {'request': request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        product = Product.object.get(pk=pk)
        product.title = request.data['title']
        product.price = request.data['price']
        product.location = request.data['location']
        product.image_path = request.data['image_path']
        product.product_type_id = request.data['product_type_id']
        product.description = request.data['description']
        product.quantity = request.data['quantity']
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        products = Product.objects.all()

        location = self.request.query_params.get('location', None)
        product = self.request.query_params.get('title', None)
        if location is not None:
            products = Product.objects.filter(location__icontains=location)
        elif product is not None:
            products = Product.objects.filter(title__icontains=product)

        serializer = ProductSerializer(
            products, many=True, context={'request': request}
        )
        return Response(serializer.data)