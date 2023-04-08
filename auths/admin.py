from django.contrib import admin
from .models import User, Department

from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "name")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_admin", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "name", "is_staff",
                "is_active", "is_admin", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
