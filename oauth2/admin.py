from django.contrib import admin
from django.contrib.auth.models import User
from oauth2.models import Router
from oauth2app.models import Client, Code, AccessToken

admin.site.unregister(User)

def clean_cascade_delete(modeladmin, request, queryset): 
    for i in queryset: 
	i.delete()
clean_cascade_delete.short_description = "Delete users and associated models (Router object)"


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
        (None, 	{'fields': ['username', 'email', 'is_superuser']})
    ]
    inlines = [RouterInline, ClientInline, CodeInline, AccessTokenInline]
    actions = [clean_cascade_delete]
    
admin.site.disable_action('delete_selected')

admin.site.register(User, UserAdmin)
