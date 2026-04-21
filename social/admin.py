from django.contrib import admin
from social.models import User, Post, Comment, Reaction, Group, Membership

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Group)
admin.site.register(Membership)

# Register your models here.
