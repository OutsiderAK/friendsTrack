from django.contrib import admin

# Register your models here.

from proj_twit.models import User, Post, PostAdmin, Comment, CommentAdmin, Message, MessageAdmin

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Message, MessageAdmin)
