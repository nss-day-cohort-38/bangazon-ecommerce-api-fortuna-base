from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Order, Customer
from ecommerceapi.models import Order_Product

class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name = 'order',
            lookup_field = 'id'
        )
        fields = ('id', 'created_at', 'customer_id', 'payment_type_id', 'products', 'customer')
        depth = 1

class Orders(ViewSet):

    def create(self, request):
        new_order = Order()
        new_order.created_at = request.data['created_at']
        new_order.customer_id = request.data['customer_id']
        new_order.payment_type_id = request.data['payment_type_id']
        new_order.save()
        serializer = OrderSerializer(new_order, context = {'request': request})
        return Response(serializer.data)
        
    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        order.created_at = request.data['created_at']
        order.customer_id = request.data['customer_id']
        order.payment_type_id = request.data['payment_type_id']
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        

    def partial_update(self, request, pk=None, partial=True):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order, context={'request': request}, partial=True)
        order.payment_type_id = request.data['payment_type']
        order.save()   
    
        return Response({}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def list(self, request):
        customer = Customer.objects.get(user = request.auth.user)
        orders = Order.objects.filter(customer = customer)
        payment_type = self.request.query_params.get('payment_type', None)
        # customer = self.request.query_params.get('customer', None)
        if payment_type is not None:
            orders = orders.filter(payment_type__id=payment_type)
        if customer is not None:
            orders = orders.filter(customer__id=customer)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)