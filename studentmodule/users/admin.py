from django.contrib import admin
from .models import Users, Program

admin.site.register(Users)
admin.site.register(Program)


# Optional: Customize the admin interface for better usability
# You can create ModelAdmin classes to customize how models are displayed
# in the admin site (e.g., list_display, search_fields, list_filter).

# Example customization for Users:
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('uid', 'role', 'firstname', 'lastname', 'email')
#     list_filter = ('role',)
#     search_fields = ('firstname', 'lastname', 'email')
# admin.site.register(Users, UsersAdmin)

# Example customization for Program:
# class ProgramAdmin(admin.ModelAdmin):
#     list_display = ('pid', 'description')
#     search_fields = ('description',)
# admin.site.register(Program, ProgramAdmin)
