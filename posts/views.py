from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post, Like
from .forms import PostForm, UserSignUp, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404
from django.utils import timezone
from django.db.models import Q #multiple quueries for search
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate #functions provided by django. login user, logout user, authenticate takes credentials and checks to see if password is corrent

# Create your views here.

def usersignup(request):
	context = {}
	form = UserSignUp()
	context['form'] = form #adding to dictionary

	if request.method == "POST":
		form = UserSignUp(request.POST) #retireve the data to form
		if form.is_valid():
			user=form.save(commit=False)
			username = user.username
			password = user.password

			user.set_password(password) #hash the password
			user.save()

			auth = authenticate(username=username, password=password)
			login(request, auth)

			return redirect("post:list")
		messages.warning(request, form.errors)
		return redirect("post: signup")
	return render(request,"signup.html", context)

def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form

	if form.is_valid():
		some_username = form.cleaned_data['username']
		some_password = form.cleaned_data['password']

		auth = authenticate(username=some_username, password=some_password)
		if auth is not None:
			login(request, auth)
			return redirect("post:list")

		messages.warning(request, "Incorrect")
		return redirect("post:login")
	return render(request, 'login.html', context)

def userlogout(request):
	logout(request)
	return redirect("post:login")

def post_detail(request, post_slug):
	object_detail = get_object_or_404(Post, slug=post_slug)
	if object_detail.publish > timezone.now().date() or object_detail.draft:
		if not (request.user.is_staff or request.user.is_superuser):
			raise Http404

	if request.user.is_authenticated():
		if Like.objects.filter(post=object_detail, user=request.user).exists():
			liked = True
		else:
			liked = False
	#like_count = Like.objects.filter(post=object_detail).count()
	like_count = object_detail.like_set.count()
	context = {"object": object_detail, "liked": liked, "like_count": like_count}
	return render(request, 'detail.html', context)

def post_list(request):
	today = timezone.now().date()
	object_list = Post.objects.filter(draft=False).filter(publish__lte=today)
	if request.user.is_staff or request.user.is_superuser:
		object_list = Post.objects.all()


	query = request.GET.get('q')
	if query:
		object_list = object_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()
	paginator = Paginator(object_list, 2)
	page = request.GET.get('page')
	try:
		object_list = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		object_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		object_list = paginator.page(paginator.num_pages)
	context = {"objects": object_list,
				"today": today,
				"user": request.user,}

	return render(request, 'list.html', context)

def post_create(request):
	if not request.user.is_staff: #from field in the user model. Django user model documentation
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		item = form.save(commit=False) #retrieve the object, just don't save it yet
		item.author = request.user
		item.save()
		messages.success(request, "ADDED")
		return redirect("post:list")
	context = {"form": form}
	return render(request, 'create.html', context)

def post_update(request, post_slug):
	item = Post.objects.get(slug=post_slug)

	form = PostForm(request.POST or None,  request.FILES or None, instance=item)

	if form.is_valid():
		form.save()
		messages.info(request, "UPDATED")
		return redirect("post:list")

	context = {"form":form,
			   "item": item}

	return render(request, 'update.html', context)

def post_delete(request, post_slug):
	item = Post.objects.get(slug=post_slug).delete()
	return redirect("post:list")

def ajax_like(request, post_slug): #likes count
    post_object = Post.objects.get(slug=post_slug)
    new_like, created = Like.objects.get_or_create(user=request.user, post=post_object)

    if created:
        action="like"
    else:
        new_like.delete()
        action="unlike"

    post_like_count = post_object.like_set.all().count()
    response = {
        "action": action,
        "post_like_count": post_like_count,
    }
    return JsonResponse(response, safe=False)



