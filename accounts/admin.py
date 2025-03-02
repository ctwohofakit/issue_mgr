from django.contrib import admin
from .models import Role,Team,CustomUser
# Register your models here.

admin.site.register(Role)
admin.site.register(Team)
admin.site.register(CustomUser)
