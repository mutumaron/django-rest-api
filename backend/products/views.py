from rest_framework import authentication,generics,permissions
from django.views import View
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


from .models import Product
from .serializers import ProductSerializer
from .permissions import IsStaffEditorPermission

class ProductCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    authentication_classes=[authentication.SessionAuthentication]
    permission_classes=[IsStaffEditorPermission]
    
    def perform_create(self, serializer):
        title=serializer.validated_data.get('title')
        content=serializer.validated_data.get('content') or None
        if content is None:
            content=title
        serializer.save(content=content)
        

# class ProductListAPIView(generics.ListAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
    


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'
    
    def perform_update(self, serializer):
        instance=serializer.save()
        if not instance.content:
            instance.content=instance.title
    
class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'
    
    def perform_destroy(self, instance):
        super().perform_destroy(instance)

# @api_view(['GET', 'POST'])
# def product_view(request, pk=None):
#     method = request.method
#     if method == "GET":
#         if pk is not None:
#             # detail view
#             product_obj = get_object_or_404(Product, pk=pk)
#             data = ProductSerializer(product_obj).data

#             return Response(data)

#         # list view
#         queryset = Product.objects.all()
#         data = ProductSerializer(queryset, many=True).data
#         return Response(data)

#     if method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             # print(serializer.data)
#             # print(serializer.validated_data)
#             serializer.save()
#             return Response(serializer.data)
#         return Response({"invalid": "not good data"}, status=400)
