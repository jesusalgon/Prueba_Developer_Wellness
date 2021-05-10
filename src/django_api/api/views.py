from django.http import JsonResponse
from rest_framework import viewsets, status, generics
from . import models
from . import serializers
from . import filters


class DataViewSet(viewsets.ModelViewSet):
    queryset = models.ElectricityConsumption.objects.all()
    serializer_class = serializers.DataSerializer
    filterset_class = filters.DateTimeFilter

    def create(self, request, *args, **kwargs):
        serializer = serializers.DataSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.validated_data
        instance, created = models.ElectricityConsumption.objects.get_or_create(**serialized_data)
        if created:
            serializer.save()
            created_message = {
                'status_code': 201,
                'detail': f'Object created with id: {instance.id}'
            }
            print(instance)
            return JsonResponse(created_message, status=status.HTTP_201_CREATED)
        else:
            error_message = {
                'status_code': 409,
                'detail': 'Error: Duplicate value cannot be crated'
            }
            return JsonResponse(error_message, status=status.HTTP_409_CONFLICT)


class UpdateDataView(generics.UpdateAPIView):
    queryset = models.ElectricityConsumption.objects.all()
    serializer_class = serializers.DataSerializer
