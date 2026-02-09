from django.contrib import admin
from src.models.location import Region, Province, Municipality, Barangay

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region")
    search_fields = ("name", "region__name")
    list_filter = ("region",)

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "province")
    search_fields = ("name", "province__name")
    list_filter = ("province",)

@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "municipality")
    search_fields = ("name", "municipality__name")
    list_filter = ("municipality",)
