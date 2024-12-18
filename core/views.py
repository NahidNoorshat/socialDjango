from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from .models import Profile, Post, Likepost, FollowersCount
from django.contrib.auth.decorators import login_required
from itertools import chain
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = request.user
    profiel_object = Profile.objects.get(user=user_object)

    post = Post.objects.all()

    return render(request, 'index.html', {'profiel_object': profiel_object, 'post':post})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    like_filter = Likepost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        like_post = Likepost.objects.create(post_id=post_id, username=username)
        like_post.save()

        post.no_of_like = post.no_of_like+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_like = post.no_of_like-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def profile(request, pk):
    user_object =  User.objects.get(username=pk)
    profile_object = Profile.objects.get(user=user_object)
    post_object = Post.objects.filter(user = pk)
    user_post_lenth = len(post_object)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = "Unfollow"
    
    else:
        button_text = "Follow"


    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))


    context = {
        "user_object": user_object,
        "profile_object": profile_object,
        "post_object": post_object,
        "user_post_lenth": user_post_lenth,
        "button_text" : button_text,
        "user_followers": user_followers,
        "user_following": user_following,
        


    }
    

    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def follow(request):
    if request.method == "POST":
        follower  = request.POST['follower']
        user = request.POST['user']
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)

        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')



def signup(request):
    if request.method == "POST":
        username = request.POST['usernme']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                mesages.info(request, "Username Taken")
                

            else:
                user = User.objects.create_user(username=username, email=email,password=password)
                user.save()

                #login user

                login_user = auth.authenticate(username=username, password=password)
                auth.login(request, login_user)

                # create a profile for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('/setting')

        else:
            messages.info(request, "Password not Matching")
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['usernme']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            return redirect('/')
        else:
            messages.info(request, "Cradential Dosen't match")
            return redirect('/signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('/signin')

@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        elif request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('/setting')
    return render(request, 'setting.html', {'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('post_image')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')

    else:
        return redirect('/')