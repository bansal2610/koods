from django.contrib import admin

from uploads.models import *


class YourModelAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )

admin.site.register(Industry, YourModelAdmin)

class YourModelAdmin(admin.ModelAdmin):
    search_fields = (
        "data",
    )

admin.site.register(skil, YourModelAdmin)


admin.site.register(Profile)