from django.db import models


class ElectricityConsumption(models.Model):
    date = models.DateField()
    time = models.TimeField()
    energy = models.FloatField()
    reactive_energy = models.FloatField()
    power = models.FloatField()
    maximeter = models.FloatField()
    reactive_power = models.FloatField()
    voltage = models.FloatField()
    intensity = models.FloatField()
    power_factor = models.FloatField()

    class Meta:
        managed = False
        db_table = 'electricity_consumption'
