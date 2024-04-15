from django.contrib import admin

from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    readonly_fields = ('created_at',) 
    fieldsets = (
        
        (
            'Individuelle Daten',
            {
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'is_verified',
                    'password',
                    'created_at',
                    'is_guest'
                )
            }
        ),
        # *UserAdmin.fieldsets,
    )
