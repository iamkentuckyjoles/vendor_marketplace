from django.contrib import admin
from .models import Region, Province, Municipality, Barangay

admin.site.register(Region)
admin.site.register(Province)
admin.site.register(Municipality)
admin.site.register(Barangay)
