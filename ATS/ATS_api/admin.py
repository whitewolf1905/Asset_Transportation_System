from django.contrib import admin
from .models import *

admin.site.register(Riders)
admin.site.register(Requesters)
admin.site.register(RidersTravelInfo)
admin.site.register(RequesterHistory)

# Register your models here.
