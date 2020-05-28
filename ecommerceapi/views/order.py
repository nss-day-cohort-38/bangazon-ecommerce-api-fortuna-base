from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Order
from ecommerceapi.models import Order_Product

class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name = 'order',
            lookup_field = 'id'
        )
        fields = ('id', 'created_at', 'customer_id', 'payment_type')

class Orders(ViewSet):

    def create(self, request):
        new_order = Order()
        new_order.created_at = request.data['created_at']
        new_order.customer_id = request.data['customer_id']
        new_order.payment_type = request.data['payment_type']
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
        order = Order.object.get(pk=pk)
        order.created_at = request.data['created_at']
        order.customer_id = request.data['customer_id']
        order.payment_type = request.data['payment_type']
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

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
        orders = Order.objects.all()
        # forgein key goes here
        paymentType = self.request.query_params.get('paymentType', None)
        customer = self.request.query_params.get('customer', None)
        if paymentType is not None:
            orders = orders.filter(paymentType__id=paymentType)
        if customer is not None:
            orders = orders.filter(customer__id=customer)

        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data)