from django.contrib import admin
from django.contrib.auth.models import User
from .models import Router
from oauth2app.models import Client, Code, AccessToken

#format admin site for management of users

admin.site.unregister(User)

#delete User object with associated Router, Client, Code, and AccessToken objects
def clean_cascade_delete(modeladmin, request, queryset): 
    for i in queryset: 
	i.delete()
clean_cascade_delete.short_description = "Delete selected users and associated objects"

class RouterInline(admin.StackedInline): 
    model = Router
    extra = 0

class ClientInline(admin.StackedInline): 
    model = Client
    extra = 0

class CodeInline(admin.StackedInline): 
    model = Code
    extra = 0

class AccessTokenInline(admin.StackedInline): 
    model = AccessToken
    extra = 0

class UserAdmin(admin.ModelAdmin): 
    fieldsets = [
        (None, 	{'fields': ['username', 'email', 'is_staff']})
    ]
    inlines = [RouterInline, ClientInline, CodeInline, AccessTokenInline]
    actions = [clean_cascade_delete]
    
admin.site.disable_action('delete_selected')

admin.site.register(User, UserAdmin)
