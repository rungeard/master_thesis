from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
# Register your models here.
admin.site.unregister(Group)

# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):        
    readonly_fields = [
        'date_joined',
        'last_login'
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Time_spend_AR)
admin.site.register(Time_spend_PDF)

admin.site.register(NASA_TLX_AR)
admin.site.register(NASA_TLX_PDF)

admin.site.register(SUS_AR)
admin.site.register(SUS_PDF)

admin.site.register(AS_AR)
admin.site.register(AS_PDF)

admin.site.register(Assembly)
admin.site.register(Custome_questions)
