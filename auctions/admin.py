from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, Bid, Comment

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Listing)
# class ListingAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Bid)
# class BidAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     pass