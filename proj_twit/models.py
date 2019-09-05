from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


# Create your models here.

class Post(models.Model):
    content = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'creation_date')


class Comment(models.Model):
    content = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'creation_date')


class Message(models.Model):
    content = models.CharField(max_length=500)
    sent_on = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="recipient", on_delete=models.CASCADE)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'sent_on')
