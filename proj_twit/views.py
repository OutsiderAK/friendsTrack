from django.shortcuts import render
from django.views import View
from proj_twit.models import Post, User, Comment, Message
import proj_twit.forms as tf
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib import messages


# Create your views here.

TimeoutScript = '''<script>
    function redirect(){
       window.location.href = "/login/";
    }
    setTimeout(redirect, 5000);
</script>'''


class RenderMainPage(View):

    def get(self, request):
        form = tf.AddPostForm()
        posts = Post.objects.all().order_by('-creation_date')
        return render(request, "index.html", {"posts": posts,
                                              "form": form})

    def post(self, request):
        form = tf.AddPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            user = request.user
            Post.objects.create(user=user, content=content)
            return HttpResponseRedirect('/')
        else:
            return render(request, "index.html", {'form': form})


class RenderLoginPage(View):

    def get(self, request):
        form = tf.LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = tf.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                messages.success(request, 'Wrong login or password')
                return HttpResponseRedirect('/login/')
            elif user is not None:
                login(request, user)
                return HttpResponseRedirect('/')


class LogoutUser(View):
    def get(self, request):
        return render(request, "logout.html")

    def post(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')


class RegisterUser(View):

    def get(self, request):
        form = tf.RegisterUserForm
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = tf.RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repassword = form.cleaned_data['repeat_password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = authenticate(username=username, password=password)
            if user is not None:
                messages.success(request, 'Taki użytkownik już istnieje')
                return HttpResponseRedirect('/register/')
            else:
                if password != repassword:
                    messages.success(request, 'Hasła nie są takie same')
                    return HttpResponseRedirect('/register/')
                else:
                    try:
                        xd = User.objects.get(username=username)
                        messages.success(request, 'Taki użytkownik już istnieje')
                        return HttpResponseRedirect('/register/')
                    except User.DoesNotExist:
                        p = User.objects.create(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                        p.set_password(password)
                        p.save()
                        log_after_reg = authenticate(username=username, password=password)
                        login(request, log_after_reg)
                        return HttpResponseRedirect('/')
        messages.success(request, 'Coś poszło nie tak')
        return HttpResponseRedirect('/register/')


class RenderComments(View):

    def get(self, request, id):
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post=post)
        form = tf.AddCommentForm
        return render(request, 'comments.html', {"post": post,
                                                 "comments": comments,
                                                 "form": form})


    def post(self, request, id):
        post = Post.objects.get(id=id)
        form = tf.AddCommentForm(request.POST)
        user = request.user
        if 'like' in request.POST:
            post.rating += 1
            post.save()
            return HttpResponseRedirect(f'/comments/{post.id}')
        elif 'unlike' in request.POST:
            post.rating -= 1
            post.save()
            return HttpResponseRedirect(f'/comments/{post.id}')
        if form.is_valid():
            comment = form.cleaned_data['comment']
            com = Comment.objects.create(content=comment, post=post, user=user)
            com.save()
            return HttpResponseRedirect(f'/comments/{post.id}')
        else:
            return HttpResponseRedirect(f'/comments/{post.id}')


class RenderMessages(View):

    def get(self, request):
        form = tf.MessageForm()
        user = request.user
        if not user.is_anonymous:
            all_msg = Message.objects.exclude(sender=user).order_by('-sent_on')
            return render(request, 'messages.html', {'form': form,
                                                     'msg': all_msg})
        else:
            return HttpResponseRedirect('/login/')


    def post(self, request):
        form = tf.MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            recipient = form.cleaned_data['recipient']
            user = request.user
            if user != recipient:
                msg = Message.objects.create(content=content, recipient=recipient, sender=user)
                messages.success(request, f'Successfully sent message to {msg.recipient}')
                return HttpResponseRedirect('/messages/')
            else:
                messages.success(request, "Don't send message to yourself")
                return HttpResponseRedirect('/messages/')
        else:
            return Http404


def easter_egg(request):
    return render(request, 'easter_egg.html')