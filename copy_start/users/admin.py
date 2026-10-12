from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
from tovar.models import KorzinaItem

class KorzinaItemInline(admin.TabularInline):
    model = KorzinaItem
    fk_name = 'us'
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = [KorzinaItemInline]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('patronymic',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('patronymic',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
