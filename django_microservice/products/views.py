import django.core.exceptions
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Products, User
from products.producer import publish
from products.serializers import ProductSerializer
import random


class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        products = Products.objects.all()
        ser = ProductSerializer(products, many=True)
        return Response(ser.data)

    def create(self, request):
        ser = ProductSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        publish('Product Created', ser.data)
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            product = Products.objects.get(id=pk)
        except django.core.exceptions.ObjectDoesNotExist:
            return Response({"Error": f"No Product for id:{pk}"})
        ser = ProductSerializer(product)
        return Response(ser.data)

    def update(self, request, pk=None):
        try:
            product = Products.objects.get(id=pk)
        except django.core.exceptions.ObjectDoesNotExist:
            return Response({"Error": f"No Product for id:{pk}"})
        ser = ProductSerializer(instance=product, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        publish('Product Updated', ser.data)
        return Response(ser.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk=None):
        try:
            product = Products.objects.get(id=pk)
        except django.core.exceptions.ObjectDoesNotExist:
            return Response({"Error": f"No Product for id:{pk}"})
        product.delete()
        publish('Product Deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):

    def get(self, request):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            "id": user.id
        })


