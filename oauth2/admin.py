from django.contrib import admin
from django.contrib.auth.models import User
from oauth2.models import Router
from oauth2app.models import Client, Code, AccessToken

admin.site.unregister(User)

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
        (None, 	{'fields': ['email', 'password']})
    ]
    inlines = [RouterInline, ClientInline, CodeInline, AccessTokenInline]


admin.site.register(User, UserAdmin)
