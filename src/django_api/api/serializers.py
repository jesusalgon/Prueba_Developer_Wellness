from rest_framework import serializers, status
from rest_framework.response import Response

from . import models


class DataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ElectricityConsumption
        fields = ('id', 'date', 'time', 'energy', 'reactive_energy', 'power', 'maximeter', 'reactive_power', 'voltage',
                  'intensity', 'power_factor')
