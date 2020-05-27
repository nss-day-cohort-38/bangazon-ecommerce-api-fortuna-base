"""Park Areas for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product_Type


class Product_Type_Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product_Type
        url = serializers.HyperlinkedIdentityField(
            view_name='product_type',
            lookup_field='id'
        )
        fields = ('id', 'name')


class Product_Types(ViewSet):

    def create(self, request):

        new_product_type = Product_Type()
        new_product_type.name = request.data["name"]
        new_product_type.save()

        Product_Type_Serializer(new_product_type, context={'request': request})

        return Response(serializer.data)

    def list(self, request):

        product_types = Product_Type.objects.all()
        serializer = Product_Type_Serializer(
            product_types, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product_type = Product_Type.objects.get(pk=pk)
            serializer = Product_Type_Serializer(
                product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        product_type = Product_Type.objects.get(pk=pk)
        product_type.name = request.data["name"]
        product_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            product_type = Product_Type.objects.get(pk=pk)
            product_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product_Type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
