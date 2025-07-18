from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    # Para que el email aparezca al crear (ADD) usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    list_display = BaseUserAdmin.list_display + ('get_role',)

    def get_role(self, obj):
        return obj.userprofile.role if hasattr(obj, 'userprofile') else ''
    get_role.short_description = 'Rol'

# Reemplazamos el admin de User estándar
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registramos UserProfile por separado
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter  = ('role',)