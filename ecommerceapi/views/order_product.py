from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product, Customer, Order, Payment_Type, Order_Product


from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Customer, Order, Order_Product, Payment_Type, Product

class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order_Product
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'order_id', 'product_id')
        
class OrderProducts(ViewSet):
    
    def create(self, request):
        customer = Customer.objects.get(user_id=request.auth.user.id)
        
        try:
            order = Order.objects.get(customer_id=customer.id, payment_type=None)
            
            new_order_product = Order_Product()
            new_order_product.product_id = request.data['product_id']
            new_order_product.order_id = order.id
            
            new_order_product.save()

            serialize = OrderProductSerializer(new_order_product, context={'request': request}) 
        except:
            new_order = Order()
            new_order.customer_id = customer.id
            new_order.save()

            new_order_product = Order_Product()
            new_order_product.product_id = request.data['product_id']
            new_order_product.order_id = new_order.id

            new_order_product.save()

            serialize = OrderProductSerializer(new_order_product, context={'request': request}) 

        return Response(serialize.data) 
    
    def retrieve(self, request, pk=None):
        try:
            order_product = Order_Product.objects.get(pk=pk)
            serializer = OrderProductSerializer(
                order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    
    def destroy(self, request, pk=None):

        try:
            orderproduct = Order_Product.objects.get(pk=pk)
            orderproduct.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order_Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        orderproduct = Order_Product.objects.get(pk=pk)
        orderproduct.order_id = request.data['order_id']
        orderproduct.product_id = request.data['product_id']
        orderproduct.rating = request.data['rating']
        orderproduct.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        
        orderproducts = Order_Product.objects.all()
      
        serializer = OrderProductSerializer(
            orderproducts, many=True, context={'request': request})
        
        return Response(serializer.data)