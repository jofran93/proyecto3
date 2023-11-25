from django.contrib import admin
from .models import UserProfile,Item,Post,Purchase


admin.site.register(UserProfile)
admin.site.register(Item)
admin.site.register(Post)
admin.site.register(Purchase)