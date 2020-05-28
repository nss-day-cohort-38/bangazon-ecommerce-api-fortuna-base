"""View module for handling requests about payment types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Payment_Type, Customer
from django.utils import timezone
from datetime import datetime


class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types
    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Payment_Type
        url = serializers.HyperlinkedIdentityField(
            view_name='payment_types',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'account_number', 'expiration_date', 'customer_id', 'created_at')
        depth = 1

class PaymentTypes(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment type
        Returns:
            Response -- JSON serialized Payment_Type instance
        """
        pass
        # try:
        #     attraction = Attraction.objects.get(pk=pk)
        #     serializer = AttractionSerializer(
        #         attraction, context={'request': request})
        #     return Response(serializer.data)
        # except Exception as ex:
        #     return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to Payment Types
        Returns:
            Response -- JSON serialized list of payment types
        """

        payment_type = Payment_Type.objects.all()

        # If customer is provided as a query parameter, then filter list of payment types by customer id
        customer = None
        if hasattr(request.auth, "user"):
            customer = Customer.objects.get(user=request.auth.user)

        if customer is not None:
            payment_type = Payment_Type.objects.filter(customer__id=customer.id)

        serializer = PaymentTypeSerializer(
            payment_type, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Payment_Type instance
        """
        new_payment_type = Payment_Type()
        new_payment_type.merchant_name = request.data["merchant_name"]
        new_payment_type.account_number = request.data["account_number"]
        new_payment_type.expiration_date = request.data["expiration_date"]
        new_payment_type.customer = Customer.objects.get(user__id=request.user.id)
        new_payment_type.created_at = datetime.now(tz=timezone.utc)
        new_payment_type.save()

        serializer = PaymentTypeSerializer(
            new_payment_type, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for payment types
        Returns:
            Response -- Empty body with 204 status code
        """
        pass
        # attraction = Attraction.objects.get(pk=pk)
        # area = ParkArea.objects.get(pk=request.data["area_id"])
        # attraction.name = request.data["name"]
        # attraction.area = area
        # attraction.save()

        # return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type
        Returns:
            Response -- 200, 404, or 500 status code
        """
        pass
        # try:
        #     attraction = Attraction.objects.get(pk=pk)
        #     attraction.delete()

        #     return Response({}, status=status.HTTP_204_NO_CONTENT)

        # except Attraction.DoesNotExist as ex:
        #     return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        # except Exception as ex:
        #     return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)