from django.db import models

class Region(models.Model):
    code = models.CharField(max_length=12, unique=True)   # e.g. 010000000
    name = models.CharField(max_length=150)               # description
    region_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "location"


class Province(models.Model):
    code = models.CharField(max_length=12, unique=True)   # e.g. 012800000
    name = models.CharField(max_length=150)               # description
    province_id = models.IntegerField(unique=True, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "location"


class Municipality(models.Model):
    code = models.CharField(max_length=12, unique=True)   # e.g. 012801000
    name = models.CharField(max_length=150)               # description
    muncity_id = models.IntegerField(unique=True, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "location"


class Barangay(models.Model):
    code = models.CharField(max_length=12, unique=True)   # e.g. 012801001
    name = models.CharField(max_length=150)               # description
    barangay_id = models.IntegerField(unique=True, null=True, blank=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "location"
